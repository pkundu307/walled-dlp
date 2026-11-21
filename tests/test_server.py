from fastapi.testclient import TestClient
from app.server import create_app
from app.decision_queue import DecisionQueue
from app.config import API_TOKEN

def test_health():
    client = TestClient(create_app(DecisionQueue()))
    assert client.get("/health").json()["status"] == "ok"

def test_clean_prompt_allowed():
    client = TestClient(create_app(DecisionQueue()))
    response = client.post(
        "/v1/scan/prompt",
        headers={"Authorization": f"Bearer {API_TOKEN}"},
        json={"text": "hello", "page": "test"}
    )
    assert response.status_code == 200
    assert response.json()["allow"] is True
