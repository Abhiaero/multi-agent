from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    """
    The state for the LangGraph multi-agent system.
    messages: List of conversation messages (managed by LangChain).
    next_agent: The name of the next agent to route to.
    context: Extracted context (e.g., from RAG) to pass between agents.
    confidence: Confidence score of the current intent/response.
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_agent: str
    context: str
    confidence: float

class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's input query")
    session_id: str = Field(default="default_session", description="Session ID for tracking history")

class ChatResponse(BaseModel):
    response: str
    agent_used: str
    confidence: float
