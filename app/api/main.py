from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import time
import os
from langchain_core.messages import HumanMessage
from app.models.state import ChatRequest, ChatResponse
from app.agents.graph import agent_graph
from app.core.metrics import log_interaction
from app.core.config import settings

app = FastAPI(title=settings.app_name)

# Mount the static directory to serve HTML/CSS/JS
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    """Serves the frontend UI on the root path."""
    return FileResponse(os.path.join(static_dir, "index.html"))
@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    try:
        # Initialize state with the user's message
        initial_state = {
            "messages": [HumanMessage(content=request.query)]
        }
        
        # Run graph
        result = agent_graph.invoke(initial_state)
        
        # Extract response and metadata
        messages = result.get("messages", [])
        final_message = messages[-1].content if messages else "No response generated."
        agent_used = result.get("next_agent", "unknown")
        confidence = result.get("confidence", 0.0)
        
        latency_ms = (time.time() - start_time) * 1000
        
        # Log to evaluation metrics DB
        log_interaction(
            session_id=request.session_id,
            query=request.query,
            response=final_message,
            agent_used=agent_used,
            confidence=confidence,
            latency_ms=latency_ms
        )
        
        return ChatResponse(
            response=final_message,
            agent_used=agent_used,
            confidence=confidence
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
