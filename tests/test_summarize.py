from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.main.requests.post")
def test_summarize_feedback(mock_post):
    # Setup mock response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "choices": [{
            "message": {
                "content": "Users love the app but had some speed issues."
            }
        }]
    }

    feedback_messages = {
        "feedback": [
            "Great app!",
            "The UI was smooth.",
            "App was a bit slow to load sometimes."
        ]
    }

    response = client.post("/summarize", json=feedback_messages)

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "success"
    assert "summary" in data
    assert "love the app" in data["summary"]

@patch("app.main.requests.post")
def test_summarize_empty_feedback(mock_post):
    feedback_messages = {
        "feedback": []
    }

    response = client.post("/summarize", json=feedback_messages)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "No feedback provided" in data["detail"]

@patch("app.main.requests.post")
def test_summarize_api_error(mock_post):
    mock_post.side_effect = Exception("API Error")
    
    feedback_messages = {
        "feedback": ["Test feedback"]
    }

    response = client.post("/summarize", json=feedback_messages)
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
