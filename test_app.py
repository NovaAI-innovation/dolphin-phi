import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.abspath('.'))

# Import your app
import app

# Mock the Llama model to avoid downloading it during tests
@pytest.fixture
def mock_llm():
    with patch('app.Llama') as mock:
        mock_instance = mock.return_value
        mock_instance.create_chat_completion.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Test response"
                    }
                }
            ]
        }
        yield mock_instance

@pytest.fixture
def client(mock_llm):
    return TestClient(app.app)

def test_greet_json(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World!"}

def test_chat_completion_with_auth(client):
    """Test the chat endpoint with authentication"""
    # Mock the authentication
    with patch.dict('os.environ', {'API_TOKEN': 'test-token'}):
        response = client.post(
            "/chat",
            params={"prompt": "Hello"},
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        assert "choices" in response.json()

def test_chat_completion_without_auth(client):
    """Test the chat endpoint without authentication"""
    response = client.post(
        "/chat",
        params={"prompt": "Hello"}
    )
    assert response.status_code == 403  # Forbidden due to missing auth

if __name__ == "__main__":
    pytest.main([__file__])