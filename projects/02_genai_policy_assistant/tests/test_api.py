import pytest
from fastapi.testclient import TestClient
from app import app  # <- now imports from the api/ directory

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body.get("ok") is True
    assert isinstance(body.get("policy_count"), int)

def test_ask_returns_contexts_or_fallback(client):
    r = client.post("/v1/ask", json={"question": "What is the remote work policy?"})
    assert r.status_code == 200
    body = r.json()
    if "contexts" in body:
        assert "draft_answer" in body
        assert isinstance(body["contexts"], list)
        assert len(body["contexts"]) >= 1
    else:
        assert "answer" in body and isinstance(body["answer"], str)

def test_search(client):
    r = client.post("/v1/search", json={"query": "password", "k": 5})
    assert r.status_code == 200
    body = r.json()
    assert body["query"] == "password"
    assert isinstance(body["results"], list)
    assert body["count"] == len(body["results"])
    assert body["count"] >= 1

def test_search_empty_query_400(client):
    r = client.post("/v1/search", json={"query": ""})
    assert r.status_code == 400
