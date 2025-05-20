from apiforge.reporter import Reporter
from typing import Any, Union, Tuple, List
from colorama import Fore, Back, Style

expected_key = Union[Tuple[str, type], Tuple[str, type, Any]]

def validate_response(data: Any, expected_keys: Union[List[expected_key], Tuple[expected_key], List[str], Tuple[str]]) -> bool:
    # Ensure API responses have expected structure
    # expected_key = (key, type) or (key, type, value) or just a string key
    r = Reporter()  # May not need

    if not expected_keys: return True

    if not isinstance(data, (dict, list, tuple)):  # Invalid data type
        # r.log_error("utils::validate_response", f"invalid data type, expected (dict, list, tuple) but recieved {type(data)}")
        return False

    if not data:  # Empty data
        # r.log_error(f"utils::validate_response", "no data passed in")
        return False

    # Handle case where expected_keys are simple strings (original behavior)
    if isinstance(expected_keys[0], str):
        if isinstance(data, dict):
            return all(key in data for key in expected_keys)
        if isinstance(data, (list, tuple)):
            for item in data:
                if not isinstance(item, dict) or not all(key in item for key in expected_keys):
                    # r.log_error(f"utils::validate_response", "either item in data is not dict or missing expected_key")
                    return False
            return True

    # Handle case where expected_keys are tuples with (key, type) or (key, type, value)
    if isinstance(data, dict):
        for item in expected_keys:
            if not isinstance(item, tuple) or len(item) not in (2, 3):
                # r.log_error(f"utils::validate_response", f"incorrect usage of tuple: {item}")
                return False
            key, expected_type = item[0], item[1]
            if key not in data or not isinstance(data[key], expected_type):
                # r.log_error(f"utils::validate_response", f"key not in data")
                return False
            if len(item) == 3 and data[key] != item[2]:  # Check value if provided
                # r.log_error(f"utils::validate_response", "value does not match")
                return False
        return True

    if isinstance(data, (list, tuple)):
        for item in data:
            if not isinstance(item, dict):
                # r.log_error(f"utils::validate_response", "item in data is not dict")
                return False
            for ek in expected_keys:
                if not isinstance(ek, tuple) or len(ek) not in (2, 3):
                    # r.log_error(f"utils::validate_response", "item in expected_keys is incorrect")
                    return False
                key, expected_type = ek[0], ek[1]
                if key not in item or not isinstance(item[key], expected_type):
                    # r.log_error(f"utils::validate_response", "item in expected_keys is incorrect")
                    return False
                if len(ek) == 3 and item[key] != ek[2]:  # Check value if provided
                    # r.log_error(f"utils::validate_response", "item in expected_keys is incorrect")
                    return False
        return True

    return False