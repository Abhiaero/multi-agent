from langgraph.graph import StateGraph, END
from app.models.state import AgentState
from app.agents.router import intent_router_node
from app.agents.rag_agent import rag_agent_node
from app.agents.llm_agent import llm_agent_node
from app.agents.fallback_agent import fallback_agent_node

def create_agent_graph():
    """
    Builds the LangGraph state machine.
    """
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("intent_router", intent_router_node)
    workflow.add_node("rag_agent", rag_agent_node)
    workflow.add_node("llm_agent", llm_agent_node)
    workflow.add_node("fallback_agent", fallback_agent_node)

    # Set entry point
    workflow.set_entry_point("intent_router")

    # Define conditional routing from the intent router
    def router_condition(state: AgentState):
        return state.get("next_agent", "fallback_agent")

    workflow.add_conditional_edges(
        "intent_router",
        router_condition,
        {
            "rag_agent": "rag_agent",
            "llm_agent": "llm_agent",
            "fallback_agent": "fallback_agent"
        }
    )

    # Add edges from agents to END
    workflow.add_edge("rag_agent", END)
    workflow.add_edge("llm_agent", END)
    workflow.add_edge("fallback_agent", END)

    # Compile graph
    return workflow.compile()

# Singleton instance
agent_graph = create_agent_graph()
