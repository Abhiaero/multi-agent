import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage
from app.agents.router import intent_router_node

@patch("app.agents.router.get_llm")
def test_intent_router_no_messages(mock_get_llm):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = '{"next_agent": "llm_agent", "confidence": 1.0}'
    mock_llm.bind.return_value = mock_llm
    mock_get_llm.return_value = mock_llm

    state = {"messages": []}
    result = intent_router_node(state)
    assert result["next_agent"] == "llm_agent"
    assert result["confidence"] == 1.0

@patch("app.agents.router.get_llm")
def test_intent_router_rag(mock_get_llm):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = '{"next_agent": "rag_agent", "confidence": 0.95}'
    mock_llm.bind.return_value = mock_llm
    mock_get_llm.return_value = mock_llm
    
    state = {"messages": [HumanMessage(content="What is your return policy?")]}
    result = intent_router_node(state)
    
    assert result["next_agent"] == "rag_agent"
    assert result["confidence"] == 0.95

@patch("app.agents.router.get_llm")
def test_intent_router_fallback(mock_get_llm):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = '{"next_agent": "llm_agent", "confidence": 0.4}'
    mock_llm.bind.return_value = mock_llm
    mock_get_llm.return_value = mock_llm
    
    state = {"messages": [HumanMessage(content="dfsdfgsdgs")]}
    result = intent_router_node(state)
    
    # Due to low confidence (<0.6), it should default to fallback
    assert result["next_agent"] == "fallback_agent"
