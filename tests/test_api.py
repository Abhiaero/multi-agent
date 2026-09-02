import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.api.main import app
from app.models.state import ChatResponse

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch("app.api.main.agent_graph")
def test_chat_endpoint(mock_agent_graph):
    # Mock the return value of the LangGraph orchestrator
    mock_message = MagicMock()
    mock_message.content = "This is a mock response from the LLM."
    
    mock_agent_graph.invoke.return_value = {
        "messages": [mock_message],
        "next_agent": "llm_agent",
        "confidence": 0.95
    }
    
    request_data = {
        "query": "Hello, how are you?",
        "session_id": "test_session_123"
    }
    
    response = client.post("/chat", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "This is a mock response from the LLM."
    assert data["agent_used"] == "llm_agent"
    assert data["confidence"] == 0.95
    
    # Verify the graph was called
    mock_agent_graph.invoke.assert_called_once()
