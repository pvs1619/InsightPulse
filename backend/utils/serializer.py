import math
import numpy as np
import pandas as pd
from typing import Any

def sanitize_json_value(val: Any) -> Any:
    """
    Recursively sanitizes values to ensure 100% JSON compliance:
    - Converts NaN / Inf floats to None
    - Converts NumPy scalars to native Python int/float/bool
    - Converts Pandas Timestamps and Datetime to ISO formatted strings
    - Recursively processes dicts and lists
    """
    if val is None:
        return None
    
    # Handle float / numpy float NaN and Inf
    if isinstance(val, (float, np.floating)):
        if math.isnan(val) or math.isinf(val) or np.isnan(val) or np.isinf(val):
            return None
        return float(val)

    # Handle integers
    if isinstance(val, (int, np.integer)):
        return int(val)

    # Handle booleans
    if isinstance(val, (bool, np.bool_)):
        return bool(val)

    # Handle datetime / timestamp
    if isinstance(val, (pd.Timestamp, np.datetime64)):
        try:
            return pd.to_datetime(val).strftime("%Y-%m-%d")
        except Exception:
            return str(val)

    # Handle dictionaries
    if isinstance(val, dict):
        return {str(k): sanitize_json_value(v) for k, v in val.items()}

    # Handle lists / tuples / sets / numpy arrays
    if isinstance(val, (list, tuple, set, np.ndarray)):
        return [sanitize_json_value(item) for item in val]

    return val
