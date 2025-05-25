import pytest
from apiforge.core import APIForge
from apiforge.reporter import Reporter

EXPECTED_KEYS = ["id", "title", "body", "userId"]
PAYLOAD = {"title": "foo", "body": "bar", "userId": 1}

@pytest.fixture
def api_forge():
    return APIForge.from_config("configs/api_config.yaml")

def test_get_posts(api_forge):
    data = api_forge.run_test("GET", "posts", expected_status=200, expected_keys=EXPECTED_KEYS)
    assert isinstance(data, list)
    for i in data: assert isinstance(i, dict)   # Returns a list of dictionaries
    assert len(data) > 0

def test_update_posts(api_forge):
    data = api_forge.run_test("PUT", "posts/1", json=PAYLOAD, expected_status=200, expected_keys=EXPECTED_KEYS)
    assert isinstance(data, dict)
    assert data.get("title") == "foo"

def test_post_deletion(api_forge):
    data = api_forge.run_test("DELETE", "posts/1", expected_status=200, expected_keys=[])
    assert isinstance(data, dict)
    assert data == {}

def test_invalid_method(api_forge):
    with pytest.raises(ValueError): api_forge.run_test("INVALID", "null")

def test_post_creation(api_forge):
    data = api_forge.run_test("POST", "posts", json=PAYLOAD, expected_status=201, expected_keys=EXPECTED_KEYS)
    assert data["title"] == "foo"

def test_run_config_tests(api_forge: APIForge, tmp_path):
    reporter = Reporter(str(tmp_path))
    results = api_forge.run_config_tests("configs/api_config.yaml", reporter)
    assert len(results) == 4

def test_response_val_success(api_forge):
    data = api_forge.run_test("GET", "posts/1", expected_status=200, expected_keys=EXPECTED_KEYS)
    assert isinstance(data, dict)
    assert "id" in data and "title" in data

def test_response_val_fail(api_forge):
    with pytest.raises(AssertionError):
        api_forge.run_test("GET", "posts/1", expected_status=200, expected_keys=["missing"])

def test_query_params(api_forge):
    params = {"userId": 1}
    data = api_forge.run_test("GET", "posts", params=params, expected_status=200, expected_keys=EXPECTED_KEYS)
    assert isinstance(data, list)
    assert len(data) > 0
    for item in data:
        assert isinstance(item, dict)
        assert item["userId"] == 1

def test_response_val_types(api_forge):
    expected_keys = [("id", int, 1), ("title", str, "foo")]
    expected_keys_l = (("id", int, 1), ("title", str, "foo"))
    data = api_forge.run_test("PUT", "posts/1", json=PAYLOAD, expected_status=200, expected_keys=expected_keys)
    data_l = api_forge.run_test("PUT", "posts/1", json=PAYLOAD, expected_status=200, expected_keys=expected_keys_l)
    assert isinstance(data, dict)
    assert isinstance(data_l, dict)
    assert data.get("title") == "foo"
    assert data_l.get("title") == "foo"

def test_network_failures(api_forge):
    pass

def test_invalid_endpoint(api_forge):
    pass