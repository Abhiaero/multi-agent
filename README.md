# Multi-Agent Conversational AI Orchestration Platform

A production-grade, scalable multi-agent platform using Gemini Pro, LangGraph, and FastAPI.

## Architecture

```mermaid
graph TD
    User([User]) --> API[FastAPI /chat]
    API --> Graph[LangGraph Orchestrator]
    Graph --> Router[Intent Router]
    
    Router -->|RAG needed| RAG[RAG Agent]
    Router -->|General chat| LLM[LLM Agent]
    Router -->|Low confidence/Out of scope| Fallback[Fallback Agent]
    
    RAG --> Chroma[(ChromaDB Vector Store)]
    RAG --> GenAI[Gemini 1.5 Pro]
    LLM --> GenAI
    
    RAG --> Response[Final Response]
    LLM --> Response
    Fallback --> Response
    
    Response --> API
    API --> Metrics[(SQLite Metrics Log)]
    API --> User
```

## Features
- **Intent Routing**: Analyzes user queries and routes them to the most appropriate specialized agent.
- **RAG Integration**: Uses Google Generative AI Embeddings with ChromaDB for highly-efficient vector context retrieval.
- **Fallback Simulation**: Handles out-of-scope or low-confidence queries gracefully.
- **State Management**: LangGraph manages conversation state across turns and agents.
- **Evaluation**: Logs latency, confidence, and agent usage to a local SQLite database for offline evaluation.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY="your_google_ai_studio_api_key"
   ```

3. **Run Tests**
   ```bash
   pytest
   ```

4. **Run the Server Locally**
   ```bash
   uvicorn app.api.main:app --reload
   ```

5. **Interact via API**
   Open `http://127.0.0.1:8000/docs` to test the API in your browser.

## Deployment
This project includes a `Dockerfile` ready for deployment on free tiers like Render, Railway, or HuggingFace Spaces.
Just provide the `GEMINI_API_KEY` as an environment variable in your deployment platform.

## 💡 How to Use the Multi-Agent AI (With Examples!)

This platform intelligently routes your questions to different AI "agents" behind the scenes based on what you ask.

### Accessing the Web UI
Once the server is running, simply open your browser and navigate to:
**`http://127.0.0.1:8000/`**

You will be greeted by a beautiful, glassmorphism chat interface where you can interact directly with the system! 

### Accessing the API directly
If you prefer to test the API endpoints instead, you can open the interactive documentation at `http://127.0.0.1:8000/docs`, or send POST requests to the `/chat` endpoint. For example, using `curl`:
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?", "session_id": "user_123"}'
```

### Examples of Questions to Ask

Because of our LangGraph Intent Router, the system handles different types of questions dynamically:

**1. General Conversation (Handled by `LLM Agent`)**
- *"Hello! How are you doing today?"*
- *"Can you explain quantum computing to a 5-year-old?"*
- *"Write a short poem about a robot learning to love."*

*(Expectation: The Router will see this as general knowledge/chat and instantly route it to the LLM Agent for a creative response).*

**2. Document Specific Questions (Handled by `RAG Agent`)**
*(Note: To test this, you first need to add some `.txt` files to a folder and run the `scripts/ingest_docs.py` script to load them into the database).*
- *"According to the company handbook, what is the remote work policy?"*
- *"Based on the uploaded documents, what are the key features of our new product?"*
- *"Summarize the meeting notes from yesterday."*

*(Expectation: The Router will identify that you are asking for specific factual information, query the ChromaDB vector database, and route it to the RAG Agent to construct an answer based strictly on your files).*

**3. Nonsense or Out of Scope (Handled by `Fallback Agent`)**
- *"asdfasdfasdfasdf"*
- *"Can you predict the winning lottery numbers for tomorrow?"*

*(Expectation: The Router will have very low confidence in understanding your intent or detect it as out-of-bounds, and will safely route you to the Fallback Agent which will gracefully decline or simulate human escalation).*
