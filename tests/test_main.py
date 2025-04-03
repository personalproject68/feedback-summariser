from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_submit_and_retrieve_feedback():
    # Step 1: Submit feedback
    response = client.post("/submit", json={
        "name": "Venky",
        "message": "This is magic!ß"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["name"] == "Venky"

    # Step 2: Check that it was stored
    response = client.get("/messages")
    assert response.status_code == 200
    messages = response.json()
    assert messages["count"] > 0
    assert any(msg["name"] == "Venky" for msg in messages["messages"])