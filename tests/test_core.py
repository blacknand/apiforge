import pytest
import requests
from apiforge.core import APIForge
from apiforge.reporter import Reporter

EXPECTED_KEYS = ["id", "title", "body", "userId"]
PAYLOAD = {"title": "foo", "body": "bar", "userId": 1}

@pytest.fixture
def api_forge():
    return APIForge.from_config("configs/open_api_config.yaml")

def test_get_posts(api_forge):
    data = api_forge.run_test("GET", "posts", expected_status=200, expected_keys=EXPECTED_KEYS)
    assert isinstance(data, list)
    for i in data: assert isinstance(i, dict)   # Returns a list of dictionaries
    assert len(data) > 0

def test_update_posts(api_forge):
    data = api_forge.run_test("PUT", "posts/1", json=PAYLOAD, expected_status=200, expected_keys=EXPECTED_KEYS)
    assert isinstance(data, dict)
    assert data.get("title") == "foo"

def test_patch(api_forge):
    data = api_forge.run_test("PATCH", "posts/1", json={"title": "foo10"}, expected_status=200, expected_keys=EXPECTED_KEYS)
    assert isinstance(data, dict)
    assert data.get("title") == "foo10"

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
    results = api_forge.run_config_tests("configs/open_api_config.yaml", reporter=reporter)
    assert len(results) == 4

def test_response_val_success(api_forge):
    data = api_forge.run_test("GET", "posts/1", expected_status=200, expected_keys=EXPECTED_KEYS)
    assert isinstance(data, dict)
    assert "id" in data and "title" in data

def test_response_val_fail(api_forge):
    with pytest.raises(RuntimeError):
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

def test_network_failures(api_forge, mocker):
    mocked_request = mocker.patch.object(
        api_forge.session,
        "request",
        side_effect=requests.ConnectionError("Network failure")
    )

    with pytest.raises(RuntimeError, match="API request failed after retries: Network failure"):
        api_forge.run_test(
            method="GET",
            endpoint="/posts",
            params={"userId": 1},
            expected_keys=EXPECTED_KEYS,
            expected_status=200
        )

    assert mocked_request.call_count == 3
    assert mocked_request.call_args_list[0] == mocker.call(
        "GET",
        "https://jsonplaceholder.typicode.com/posts",
        params={"userId": 1},
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
    )

def test_invalid_endpoint(api_forge, mocker):
    mock_response = mocker.MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"

    mocker.patch.object(
        api_forge.session,
        "request",
        return_value=mock_response
    )

    with pytest.raises(RuntimeError, match="API error: Endpoint not found: 404"):
        api_forge.run_test(
            method="GET",
            endpoint="/non_existent",
            params={"userId": 1},
            expected_status=200,
            expected_keys=EXPECTED_KEYS
        )

    assert api_forge.session.request.call_count == 1
    assert api_forge.session.request.call_args == mocker.call(
        "GET",
        "https://jsonplaceholder.typicode.com/non_existent",
        params={"userId": 1},
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
    )

def test_generated_tests(api_forge):
    results = api_forge.run_generated_tests("configs/open_api_config.yaml")
    assert isinstance(results, list)
    assert len(results) >= 1  
    for result in results:
        assert isinstance(result, dict) or isinstance(result, list)
        if isinstance(result, list):
            for item in result:
                assert isinstance(item, dict)
                for key in EXPECTED_KEYS:
                    assert key in item

def test_osa_dict():
    mock_spec = {
        "openapi": "3.0.3",
        "info": [{"title": "test_osa_dict API"}, {"description": "In memory test dict"}],
        "servers": [{"url": "https://api.example.com"}],
        "paths": {
            "/test": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object", "required": ["id"]}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    api_forge = APIForge.from_config(mock_spec)
    results = api_forge.run_generated_tests(mock_spec)
    assert isinstance(results, list)
    assert len(results) == 1
    assert isinstance(results[0], list)
    for item in results[0]:
        assert isinstance(item, dict)
        for key in EXPECTED_KEYS:
            assert key in item