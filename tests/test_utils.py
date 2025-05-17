import pytest
from apiforge.utils import validate_response
from apiforge.reporter import Reporter
from .test_core import EXPECTED_KEYS, PAYLOAD

def test_valid_response():
    data = {"title": "foo", "body": "bar", "userId": 1}
    expected_keys = ["title", "body"]
    assert validate_response(data, expected_keys=expected_keys) is True

def test_missing_keys():
    data = {"title": "foot"}
    expected_keys = ["title", "body"]
    expected_keys_t = ("title", "body")
    assert validate_response(data, expected_keys=expected_keys) is False
    assert validate_response(data, expected_keys=expected_keys_t) is False

def test_invalid_dict():
    data = 42
    data_str = "string"
    data_null = None
    expected_keys = ["title"]
    assert validate_response(data, expected_keys=expected_keys) is False
    assert validate_response(data_str, expected_keys=expected_keys) is False
    assert validate_response(data_null, expected_keys=expected_keys) is False

def test_empty_keys():
    data = {"title": "foot"}
    expected_keys = []
    expected_keys_t = ()
    assert validate_response(data, expected_keys=expected_keys) is True
    assert validate_response(data, expected_keys=expected_keys_t) is True

def test_expected_keys():
    data = {"title": "foot", "body": "bar"}
    expected_keys_list = ["title", "body"]
    expected_keys_tuple = ("title", "body")

    assert validate_response(data, expected_keys=expected_keys_list) is True
    assert validate_response(data, expected_keys=expected_keys_tuple) is True
    assert validate_response(PAYLOAD, expected_keys=("title", "body", "userId")) is True

def test_list_of_dicts():
    data = [{"title": "foo", "body": "bar"}, {"title": "baz", "body": "qux"}] 
    expected_keys = ["title", "body"]
    assert validate_response(data, expected_keys=expected_keys) is True

# NOTE: Testing an empty list may be tested in the future,
# NOTE: but is currently unecessary since validate_response
# NOTE: should hanlde an empty payload (data) regardless
@pytest.mark.xfail(reason="Expected behaviour, may change in future however")
def test_empty_list():
    data = []
    assert validate_response(data, expected_keys=[]) is False

def test_list_w_non_dict_items():
    data=[{"title": "foo"}, 42]
    expected_keys=["title"]
    assert validate_response(data, expected_keys=expected_keys) is False

def test_large_dataset():
    data = [{"title": "foo", "body": "bar"}] * 100
    expected_keys = ["title", "body"]
    assert validate_response(data, expected_keys=expected_keys) is True