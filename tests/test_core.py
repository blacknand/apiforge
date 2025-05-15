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