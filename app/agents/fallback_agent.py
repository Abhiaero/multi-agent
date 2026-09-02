from langchain_core.messages import AIMessage
from app.models.state import AgentState

def fallback_agent_node(state: AgentState) -> dict:
    """
    Handles fallback scenarios (e.g., low confidence, out-of-scope).
    Simulates human escalation.
    """
    response_msg = (
        "I'm sorry, but I'm not entirely sure how to help with that based on my current knowledge. "
        "I am transferring this conversation to a human agent who can assist you further."
    )
    return {"messages": [AIMessage(content=response_msg)]}
