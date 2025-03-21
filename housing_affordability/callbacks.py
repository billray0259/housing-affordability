from dash.dependencies import Input, Output, State, ALL
from dash import dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objs as go  # new import for plotly

def register_callbacks(app):

    @app.callback(
        Output("output", "children"),
        [Input("input", "value")]
    )
    def update_output(value):
        return value

    # New callback to open the update modal on node click
    @app.callback(
        [Output("update-modal", "is_open"),
         Output("update-node-name", "value"),
         Output("update-node-value", "value"),
         Output("selected-node-id", "data")],
        [Input("cytoscape", "tapNode")],
        [State("update-modal", "is_open")]
    )
    def open_update_modal(tapNode, is_open):
        if not tapNode:
            return no_update, no_update, no_update, no_update
        label = tapNode['data'].get("label", "")
        node_id = tapNode['data'].get("id")
        if ':' in label:
            name, value = label.split(":", 1)
            return True, name.strip(), value.strip(), node_id
        else:
            return True, label, "", node_id

    # The callback for adding new nodes (unchanged)
    @app.callback(
        Output("cytoscape", "elements"),
        [Input("add-node", "n_clicks")],
        [State("node-name", "value"),
         State("node-value", "value"),
         State("add-node", "children"),
         State("cytoscape", "elements"),
         State("selected-node-id", "data")]
    )
    def modify_node(n_clicks, node_name, node_value, btn_text, elements, selected_node_id):
        if not n_clicks:
            return no_update
        updated_elements = elements.copy()  # shallow copy is fine for simple dicts
        if btn_text == "Add Node":
            # Generate a unique id
            existing_ids = {elem['data']['id'] for elem in updated_elements if 'id' in elem['data']}
            new_id = "node0"
            k = 0
            while new_id in existing_ids:
                k += 1
                new_id = f"node{k}"
            new_label = f"{node_name}: {node_value}"
            updated_elements.append({'data': {'id': new_id, 'label': new_label}})
        return updated_elements

    # New callback to update a node from the modal (or close the modal)
    @app.callback(
        [Output("cytoscape", "elements"),
         Output("update-modal", "is_open")],
        [Input("update-node-btn", "n_clicks"),
         Input("close-modal-btn", "n_clicks")],
        [State("update-node-name", "value"),
         State("update-node-value", "value"),
         State("cytoscape", "elements"),
         State("selected-node-id", "data")]
    )
    def update_node(update_clicks, close_clicks, node_name, node_value, elements, selected_node_id):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == "close-modal-btn":
            # Close modal without updating
            return no_update, False
        elif trigger_id == "update-node-btn" and selected_node_id:
            updated_elements = elements.copy()
            for elem in updated_elements:
                if elem['data']['id'] == selected_node_id:
                    elem['data']['label'] = f"{node_name}: {node_value}"
                    break
            return updated_elements, False
        return no_update, no_update