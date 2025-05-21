from typing import Any, Union, Tuple, List

expected_key = Union[Tuple[str, type], Tuple[str, type, Any]]

def validate_response(data: Any, expected_keys: Union[List[expected_key], Tuple[expected_key], List[str], Tuple[str]]) -> bool:
    # Ensure API responses have expected structure
    if not expected_keys: return True
    if not isinstance(data, (dict, list, tuple)): return False
    if not data: return False

    # First check if all expected_keys are present in data
    if isinstance(expected_keys[0], str):   # If first item is str, assume all are str
        if isinstance(data, dict): return all(key in data for key in expected_keys)
        if isinstance(data, (list, tuple)):
            for item in data:
                if not isinstance(item, dict) or not all(key in item for key in expected_keys): return False
            return True

    # Handle case where expected_keys are tuples with (key, type) or (key, type, value),
    # check that the key is of the expected type and optionally if the value matches the expected value
    if isinstance(data, dict):
        for item in expected_keys:
            if not isinstance(item, tuple) or len(item) not in (2, 3): return False
            key, expected_type = item[0], item[1]
            if key not in data or not isinstance(data[key], expected_type): return False
            if len(item) == 3 and data[key] != item[2]: return False
        return True

    # Same logic as above but if data is a list/tuple of dictionaries 
    if isinstance(data, (list, tuple)):
        for item in data:
            if not isinstance(item, dict): return False
            for ek in expected_keys:
                if not isinstance(ek, tuple) or len(ek) not in (2, 3): return False
                key, expected_type = ek[0], ek[1]
                if key not in item or not isinstance(item[key], expected_type): return False
                if len(ek) == 3 and item[key] != ek[2]: return False
        return True

    return False