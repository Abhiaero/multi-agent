from langchain_core.messages import SystemMessage, AIMessage
from app.core.llm import get_llm
from app.core.rag import rag_manager
from app.models.state import AgentState

RAG_PROMPT = """
You are a helpful knowledge-base agent. Answer the user's question based ONLY on the provided context.
If you cannot answer the question based on the context, state that clearly and do not make up an answer.

Context:
{context}
"""

def rag_agent_node(state: AgentState) -> dict:
    """
    Retrieves context from ChromaDB and generates an answer using the LLM.
    """
    messages = state.get("messages", [])
    last_user_message = next((m for m in reversed(messages) if m.type == "human"), None)
    
    if not last_user_message:
        return {"messages": [AIMessage(content="I didn't receive a query.")]}

    # Retrieve documents
    docs = rag_manager.retrieve(last_user_message.content)
    context_str = "\n\n".join([doc.page_content for doc in docs])
    
    # Generate response
    sys_msg = SystemMessage(content=RAG_PROMPT.format(context=context_str))
    llm = get_llm()
    
    # We pass the system message + all prior conversation history
    response = llm.invoke([sys_msg] + list(messages))
    
    return {
        "messages": [response],
        "context": context_str
    }
