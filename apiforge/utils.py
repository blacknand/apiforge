from typing import Any, List

def validate_response(data: Any, expected_keys: list) -> bool:
    if not expected_keys: return True       # No keys to check, so fine
    if not isinstance(data, (dict, list)): return False
    if isinstance(data, dict): return all(key in data for key in expected_keys)
    if not data: return False

    for item in data:
        if not isinstance(item, dict) or not all(key in item for key in expected_keys): return False
    return True