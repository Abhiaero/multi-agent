import json
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.llm import get_llm
from app.models.state import AgentState

ROUTER_PROMPT = """
You are an intelligent router for a customer support / conversational system.
Analyze the user's latest message and route to the appropriate agent.

Available Agents:
- 'rag_agent': For questions that require searching a knowledge base (e.g., company policies, specific documentation, technical guides).
- 'llm_agent': For general conversation, greetings, small talk, or general knowledge.
- 'fallback_agent': For queries that are completely out of scope, inappropriate, or if you have very low confidence in understanding the intent.

Return ONLY a JSON object with the following structure:
{
    "next_agent": "name of the agent",
    "confidence": 0.95,
    "reasoning": "brief explanation of your choice"
}
"""

def intent_router_node(state: AgentState) -> dict:
    """
    Analyzes the last message and decides which agent to route to.
    """
    llm = get_llm(temperature=0.0).bind(response_format={"type": "json_object"})
    messages = state.get("messages", [])
    if not messages:
        return {"next_agent": "llm_agent", "confidence": 1.0}
    
    last_user_message = next((m for m in reversed(messages) if m.type == "human"), None)
    if not last_user_message:
        return {"next_agent": "llm_agent", "confidence": 1.0}

    sys_msg = SystemMessage(content=ROUTER_PROMPT)
    prompt_msgs = [sys_msg, HumanMessage(content=last_user_message.content)]
    
    response = llm.invoke(prompt_msgs)
    
    try:
        # Assuming the LLM returns JSON due to prompt constraints or response_format binding
        result = json.loads(response.content)
        next_agent = result.get("next_agent", "fallback_agent")
        confidence = float(result.get("confidence", 0.0))
        
        # Override to fallback if confidence is too low
        if confidence < 0.6:
            next_agent = "fallback_agent"
            
    except Exception:
        next_agent = "fallback_agent"
        confidence = 0.0

    return {"next_agent": next_agent, "confidence": confidence}
