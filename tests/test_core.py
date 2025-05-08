import pytest
from apiforge.core import APIForge
from apiforge.reporter import Reporter

@pytest.fixture
def api_forge():
    return APIForge.from_config("configs/api_config.yaml")

def test_get_posts(api_forge):
    data = api_forge.run_test("GET", "posts", expected_status=200)
    assert len(data) > 0
    assert isinstance(data, list)

def test_invalid_method(api_forge):
    with pytest.raises(ValueError): api_forge.run_test("INVALID", "null")

def test_post_creation(api_forge):
    payload = {"title": "foo", "body": "bar", "userId": 1}
    data = api_forge.run_test("POST", "posts", json=payload, expected_status=201)
    assert data["title"] == "foo"

def test_run_config_tests(api_forge: APIForge, tmp_path):
    reporter = Reporter(str(tmp_path))
    results = api_forge.run_config_tests("configs/api_config.yaml", reporter)
    assert len(results) == 2