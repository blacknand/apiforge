import pytest
from apiforge.core import APIForge

@pytest.fixture
def api_forge():
    return APIForge("https://jsonplaceholder.typicode.com")

def test_get_posts(api_forge):
    data = api_forge.run_test("GET", "posts", expected_status=200)
    assert len(data) > 0
    assert isinstance(data, list)

def test_post_creation(api_forge):
    payload = {"title": "foo", "body": "bar", "userId": 1}
    data = api_forge.run_test("POST", "posts", json=payload, expected_status=201)
    assert data["title"] == "foo"