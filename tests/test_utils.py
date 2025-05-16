from apiforge.utils import validate_response
from .test_core import EXPECTED_KEYS

def test_valid_response():
    data = {"title": "foo", "body": "bar", "userId": 1}
    expected_keys = ["title", "body"]
    assert (validate_response(data, expected_keys=expected_keys)) is True

def test_missing_keys():
    data = {"title": "foot"}
    expected_keys = ["title", "body"]
    assert (validate_response(data, expected_keys=expected_keys)) is False

def test_invalid_dict():
    data = {"title"}
    expected_keys = ["title"]
    assert (validate_response(data, expected_keys=expected_keys)) is False

def test_empty_keys():
    data = {"title": "foot"}
    expected_keys = []
    assert (validate_response(data, expected_keys=expected_keys)) is True

def test_expected_keys():
    data = {"title": "foot", "body": "bar"}
    expected_keys_list = ["title", "body"]
    expected_keys_tuple = ("title", "body")
    assert (validate_response(data, expected_keys=expected_keys_list)) is True
    assert (validate_response(data, expected_keys=expected_keys_tuple)) is True

def test_list_of_dicts():
    data = [{"title": "foo", "body": "bar"}, {"title": "baz", "body": "qux"}] 
    expected_keys = ["title", "body"]
    assert (validate_response(data, expected_keys=expected_keys)) is True
