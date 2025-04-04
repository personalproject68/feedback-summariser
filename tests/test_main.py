import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = TestClient(app)

def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hi, I'm alive"}

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.text == '"pong"'

def test_submit_and_retrieve_feedback():
    # Step 1: Submit feedback
    response = client.post("/submit", json={
        "name": "Test User",
        "message": "This is a test message"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["name"] == "Test User"

    # Step 2: Check that it was stored
    response = client.get("/messages")
    assert response.status_code == 200
    messages = response.json()
    assert messages["count"] > 0
    assert any(msg["name"] == "Test User" for msg in messages["messages"])