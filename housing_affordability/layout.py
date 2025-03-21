# dash_app/layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_cytoscape as cyto
import json
import housing_affordability.pytorch_excel as pytorch_excel
import ast   # new import

def parse_input_nodes(value_str, valid_funcs):
    # Parses a value string and returns identifiers not named in valid_funcs.
    tree = ast.parse(value_str, mode='eval')
    inputs = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id not in valid_funcs:
            inputs.add(node.id)
    return list(inputs)

def create_layout():
    with open('/home/bill/dev/school/holt-research/housing-affordability/graph.json') as f:
        graph_data = json.load(f)
    
    computed = {}
    # First pass: assign non-code (numeric) values
    for node_id, data in graph_data.items():
        if "value" in data and not isinstance(data["value"], str):
            computed[node_id] = data["value"]
    # Second pass: evaluate code if value is a string
    for node_id, data in graph_data.items():
        if "value" in data and isinstance(data["value"], str):
            try:
                computed[node_id] = eval(
                    data["value"],
                    {k: getattr(pytorch_excel, k) for k in dir(pytorch_excel) if not k.startswith("__")},
                    computed
                )
            except Exception as e:
                computed[node_id] = f"Error: {e}"
    
    nodes = []
    edges = []
    valid_funcs = {k for k in dir(pytorch_excel) if not k.startswith("__")}
    for node_id, data in graph_data.items():
        label = f'{data.get("name", node_id)}: {computed.get(node_id, "N/A")}'
        nodes.append({'data': {'id': node_id, 'label': label}})
        # Instead of relying on an "inputs" list, parse the input nodes from the value string.
        if "value" in data and isinstance(data["value"], str):
            for src in parse_input_nodes(data["value"], valid_funcs):
                if src in graph_data:
                    edges.append({'data': {'source': src, 'target': node_id}})
    elements = nodes + edges

    return html.Div([
        dbc.Card(
            [
                dbc.CardHeader("Control Panel"),
                dbc.CardBody(
                    [
                        dcc.Input(id="node-name", type="text", placeholder="Name", className="mb-2"),
                        dcc.Input(id="node-value", type="text", placeholder="Value", className="mb-2"),
                        html.Button("Add Node", id="add-node", n_clicks=0, className="btn btn-primary")
                    ]
                )
            ],
            style={'position': 'absolute', 'top': '10px', 'left': '10px', 'zIndex': 9999, 'width': '300px'}
        ),
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,  # updated to use graph JSON and computed labels
            style={'width': '100vw', 'height': '100vh'},
            layout={
                'name': 'cose',             
                'idealEdgeLength': 100,     
                'nodeOverlap': 20,
                'refresh': 20,
                'fit': True,
                'padding': 30,
                'randomize': False
            },
            stylesheet=[
                {   # base node style
                    'selector': 'node',
                    'style': {
                        'label': 'data(label)',
                        'text-valign': 'center',
                        'color': 'black',
                        'font-size': '12px',
                        'text-outline-color': 'white',
                        'text-outline-width': 1
                    }
                },
                {   # edge style
                    'selector': 'edge',
                    'style': {
                        'target-arrow-shape': 'triangle',
                        'target-arrow-color': 'black',
                        'curve-style': 'bezier',
                        'line-color': 'black',
                    }
                }
            ]
        ),
        # New modal for updating a node
        dbc.Modal(
            [
                dbc.ModalHeader("Update Node"),
                dbc.ModalBody([
                    dcc.Input(id="update-node-name", type="text", placeholder="Name", className="mb-2"),
                    dcc.Input(id="update-node-value", type="text", placeholder="Value", className="mb-2")
                ]),
                dbc.ModalFooter([
                    html.Button("Update", id="update-node-btn", n_clicks=0, className="btn btn-primary"),
                    html.Button("Close", id="close-modal-btn", n_clicks=0, className="btn btn-secondary")
                ])
            ],
            id="update-modal",
            is_open=False
        ),
        dcc.Store(id="selected-node-id")  # New hidden store for selected node id
    ], style={'margin': '0', 'padding': '0'})
