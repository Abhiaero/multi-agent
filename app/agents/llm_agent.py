from langchain_core.messages import SystemMessage
from app.core.llm import get_llm
from app.models.state import AgentState

LLM_PROMPT = """
You are a friendly, conversational AI assistant.
Answer the user's questions clearly and concisely.
"""

def llm_agent_node(state: AgentState) -> dict:
    """
    Handles general conversational queries.
    """
    messages = state.get("messages", [])
    sys_msg = SystemMessage(content=LLM_PROMPT)
    
    llm = get_llm()
    response = llm.invoke([sys_msg] + list(messages))
    
    return {"messages": [response]}
