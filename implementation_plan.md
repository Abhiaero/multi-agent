# Goal Description

Build a production-grade **Multi-Agent Conversational AI Orchestration Platform** using free tools and the Python ecosystem. The system will route user queries across multiple agents (LLM, RAG, fallback) utilizing Gemini Pro as the primary LLM. Key features include state management, intent routing, evaluation metrics, and a scalable architecture.

## User Review Required

> [!IMPORTANT]
> Please review the proposed technology stack and the step-by-step implementation phases. This architecture aims for a balance between ease of development and production readiness, using popular open-source libraries.

## Open Questions

- Do you have your `GEMINI_API_KEY` ready to use? You can get a free one from Google AI Studio.
- For deployment, are you comfortable using Docker and deploying to Render or HuggingFace Spaces?

## Proposed Architecture and Stack

- **Core Framework**: LangGraph for multi-agent state orchestration (ideal for stateful, multi-actor applications).
- **LLM**: `langchain-google-genai` to interact with Gemini Pro.
- **RAG / Vector DB**: ChromaDB (runs locally, free) and HuggingFace `sentence-transformers` for local, cost-free embeddings.
- **Backend**: FastAPI for a high-performance REST API.
- **Memory**: LangGraph's built-in state management for short-term (message history), ChromaDB for long-term semantic retrieval.
- **Evaluation/Metrics**: Custom logging to a local SQLite database for metrics (latency, response quality, fallback rates).

## Proposed Changes / Phases

We will build this in `e:/projects/multi-agent` using the following phases. I will guide you through each phase and write the code incrementally.

### Phase 1: Project Setup & Core Architecture (Steps 1 & 2)
- Set up the Python virtual environment and `requirements.txt`.
- Establish a production folder structure (`app/`, `app/agents`, `app/core`, `app/api`, `tests/`).
- Define the core data models and configuration.

### Phase 2: LLM & RAG Integration (Steps 3 & 4)
- Implement a reusable wrapper for the Gemini Pro API.
- Set up local ChromaDB and create document ingestion, chunking, and retrieval pipelines using free HuggingFace embeddings.

### Phase 3: Multi-Agent Orchestration & Memory (Steps 5, 6 & 7)
- Build the LangGraph state machine.
- Implement specific agents/nodes:
  - **Intent Router**: Analyzes queries and routes to the appropriate agent.
  - **RAG Agent**: Handles information retrieval tasks.
  - **General LLM Agent**: Handles conversational tasks.
  - **Fallback Agent**: Handles low-confidence or unsupported queries, simulating human escalation.
- Integrate memory to pass context between turns and agents.

### Phase 4: Backend API & Evaluation (Steps 8 & 9)
- Build the FastAPI application with `/chat`, `/health`, and `/metrics` endpoints.
- Integrate the LangGraph orchestrator into the `/chat` endpoint.
- Implement an evaluation tracker (SQLite) to log latency, confidence scores, and fallback rates.

### Phase 5: Testing, Deployment & Documentation (Steps 10, 11 & 12)
- Write `pytest` unit tests for agents and the routing logic.
- Create a `Dockerfile` for containerization.
- Generate a comprehensive `README.md` and system architecture diagram (Mermaid).

## Verification Plan

### Automated Tests
- Run `pytest` to ensure all components (router, LLM wrappers, RAG pipeline) function correctly in isolation.

### Manual Verification
- Run the FastAPI server locally using `uvicorn`.
- Test endpoints using Swagger UI (`/docs`) to verify intent routing (e.g., asking a general question vs. asking about a specific document).
- Verify memory retention across multiple interactions.
- Check the SQLite database to confirm metrics are being logged correctly.
