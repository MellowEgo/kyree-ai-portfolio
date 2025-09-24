import pytest
from fastapi.testclient import TestClient
from api.app import app

@pytest.fixture(scope="module")
def client():
    # Using context manager ensures FastAPI lifespan (startup/shutdown) runs.
    with TestClient(app) as c:
        yield c

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body.get("ok") is True
    assert isinstance(body.get("policy_count"), int)

def test_ask(client):
    r = client.post("/ask", json={"question": "remote work policy"})
    assert r.status_code == 200
    assert "answer" in r.json()
