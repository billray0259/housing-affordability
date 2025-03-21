import torch

def SUM(*args):
    arr = torch.tensor(args, dtype=torch.float32)
    return torch.sum(arr)

def AVERAGE(*args):
    arr = torch.tensor(args, dtype=torch.float32)
    return torch.mean(arr)

def COUNT(*args):
    return torch.tensor(len(args), dtype=torch.float32)

def MAX(*args):
    arr = torch.tensor(args, dtype=torch.float32)
    return torch.max(arr)

def MIN(*args):
    arr = torch.tensor(args, dtype=torch.float32)
    return torch.min(arr)

def ROUND(*args, decimals=0):
    factor = 10 ** decimals
    arr = torch.tensor(args, dtype=torch.float32)
    return torch.round(arr * factor) / factor

def PRODUCT(*args):
    arr = torch.tensor(args, dtype=torch.float32)
    return torch.prod(arr)

def MEDIAN(*args):
    arr = torch.tensor(args, dtype=torch.float32)
    sorted_arr, _ = torch.sort(arr)
    n = sorted_arr.numel()
    mid = n // 2
    if n % 2 == 1:
        return sorted_arr[mid]
    return (sorted_arr[mid - 1] + sorted_arr[mid]) / 2

def VARIANCE(*args):
    arr = torch.tensor(args, dtype=torch.float32)
    return torch.var(arr, unbiased=False)

def STDEV(*args):
    return torch.sqrt(VARIANCE(*args))

def POWER(base, exponent):
    base_tensor = torch.tensor(base, dtype=torch.float32)
    exponent_tensor = torch.tensor(exponent, dtype=torch.float32)
    return torch.pow(base_tensor, exponent_tensor)

def ABS(val):
    tensor = torch.tensor(val, dtype=torch.float32)
    return torch.abs(tensor)

def GEOMEAN(*args):
    # Geometric mean: nth root of product of n numbers.
    arr = torch.tensor(args, dtype=torch.float32)
    n = arr.numel()
    # Only works for positive numbers.
    return torch.pow(torch.prod(arr), 1.0 / n)

def HARMEAN(*args):
    # Harmonic mean: n / (sum of reciprocals)
    arr = torch.tensor(args, dtype=torch.float32)
    reciprocal = 1 / arr
    return arr.numel() / torch.sum(reciprocal)

def LN(val):
    tensor = torch.tensor(val, dtype=torch.float32)
    return torch.log(tensor)

def EXP(val):
    tensor = torch.tensor(val, dtype=torch.float32)
    return torch.exp(tensor)

def SQRT(val):
    tensor = torch.tensor(val, dtype=torch.float32)
    return torch.sqrt(tensor)

def FLOOR(val):
    tensor = torch.tensor(val, dtype=torch.float32)
    return torch.floor(tensor)

def CEILING(val):
    tensor = torch.tensor(val, dtype=torch.float32)
    return torch.ceil(tensor)

def LOG10(val):
    tensor = torch.tensor(val, dtype=torch.float32)
    return torch.log10(tensor)

def MODE(*args):
    # Returns the most frequent value. In case of ties, returns one of them.
    arr = torch.tensor(args, dtype=torch.float32)
    uniques, counts = torch.unique(arr, return_counts=True)
    max_count = torch.max(counts)
    mode_candidates = uniques[counts == max_count]
    # Return the first mode candidate.
    return mode_candidates[0]

def RANK(value, *args):
    # Rank the value among others in descending order.
    arr = torch.tensor(args, dtype=torch.float32)
    # Count how many numbers are greater than value.
    higher = torch.sum(arr > value)
    # Rank is count of numbers higher plus 1.
    return higher.item() + 1