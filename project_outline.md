# Project Outline: Multi-Agent Conversational AI Platform

Welcome! This document is designed to help beginners understand exactly what this project is, how it works, and why we chose the specific tools we used to build it.

---

## 🎯 What are we building?

We have built a **Multi-Agent Conversational AI Orchestration Platform**. 
Let's break that down:
- **Conversational AI**: A chatbot that you can talk to.
- **Multi-Agent**: Instead of having one giant AI try to do everything, we have multiple smaller, specialized "AI Agents" that work together as a team. For example, one agent handles general chat, another looks up specific documents, and another acts as a router to decide who should speak.
- **Orchestration**: The system that acts as the "manager" of this team, making sure the right agent gets the right task at the right time.

When a user asks a question, our system analyzes the intent, routes the question to the best specialized agent, generates an answer, and keeps track of the conversation history.

---

## 🛠️ Tools We Used (and Why!)

This project was built entirely using **free, open-source, or free-tier** tools. Here is a breakdown of every major piece of technology in the stack:

### 1. Python 🐍
- **What it is**: The programming language used for the entire project.
- **Why we used it**: Python is the absolute industry standard for Artificial Intelligence and Machine Learning. It has the largest ecosystem of libraries for building AI apps.

### 2. Google Gemini Pro 🧠 (`langchain-google-genai`)
- **What it is**: The core "brain" of our AI. It's a Large Language Model (LLM) created by Google, similar to ChatGPT.
- **Why we used it**: Google offers generous free tiers for developers to use Gemini Pro via Google AI Studio. It is incredibly smart and fast, making it perfect for generating our chatbot's responses.

### 3. LangGraph & LangChain 🔗 (`langgraph`, `langchain-core`)
- **What it is**: Frameworks for building AI applications. LangChain gives us the building blocks to talk to LLMs, and **LangGraph** specifically helps us build "State Machines" (complex workflows where agents pass information back and forth).
- **Why we used it**: Managing conversation history, routing logic, and passing context between different AI agents from scratch is very hard. LangGraph makes it easy to define rules like: *"If the user asks about the weather, send it to Agent A. If they ask about a document, send it to Agent B."*

### 4. ChromaDB 🗄️ (`chromadb`)
- **What it is**: A Vector Database. Unlike traditional databases (which store rows and columns), vector databases store data as mathematical coordinates. 
- **Why we used it**: We use it for **RAG (Retrieval-Augmented Generation)**. It allows our AI to search through huge amounts of text and find the paragraphs that are semantically most similar to a user's question. We chose ChromaDB because it runs completely locally and for free on your machine.

### 5. HuggingFace Embeddings 🧬 (`sentence-transformers`)
- **What it is**: A tool that turns plain English text into those mathematical coordinates (called "embeddings") that ChromaDB needs.
- **Why we used it**: Typically, developers pay for tools like OpenAI Embeddings. By using HuggingFace's local sentence-transformers, we do this math locally on your own computer, keeping the project 100% free.

### 6. FastAPI ⚡ (`fastapi`, `uvicorn`)
- **What it is**: A modern framework for building backend APIs in Python.
- **Why we used it**: Once our AI is built, it needs a way to communicate with the outside world (like a website frontend or a mobile app). FastAPI lets us create a `/chat` URL endpoint that other applications can send messages to. It is incredibly fast and beginner-friendly.

### 7. Pydantic 🛡️ (`pydantic`, `pydantic-settings`)
- **What it is**: A data validation library. 
- **Why we used it**: It ensures that the data going into our API is exactly what we expect. For example, if we expect a user query to be a string of text, Pydantic will block the request if someone tries to send a number instead. It also safely manages our secret passwords (like the `GEMINI_API_KEY`).

### 8. SQLite 📊 (Built into Python)
- **What it is**: A lightweight database that stores data in a simple file.
- **Why we used it**: We use it to log "metrics" (how fast the AI responded, what the AI's confidence score was). It's built directly into Python, meaning we didn't have to install any complex database software like PostgreSQL.

### 9. Pytest 🧪 (`pytest`)
- **What it is**: A testing framework for Python code.
- **Why we used it**: To ensure our code actually works before we launch it! We wrote tests to guarantee that our "Intent Router" correctly figures out which agent should handle a specific question.

### 10. Docker 🐳
- **What it is**: A tool that packages our entire application (code, libraries, Python itself) into a single standard unit called a "container".
- **Why we used it**: It guarantees that if the app works on your computer, it will work exactly the same way on any server in the cloud. It prevents the classic "It works on my machine!" problem.

---

## 🚀 How the System Flows (Beginner's Summary)

1. **User asks a question** via the FastAPI endpoint.
2. The **Intent Router** reads the question and says: *"Hmm, does this require searching the database (RAG), general chat (LLM), or is it too confusing (Fallback)?"*
3. The Router passes the question to the **winning Agent**.
4. That Agent formulates a response (sometimes looking up context in ChromaDB).
5. The response is sent back to the user, and the interaction is logged in SQLite for us to review later!

---

## 🏃‍♂️ Step-by-Step: How to Run & What to Expect

Follow these simple steps to start the platform and interact with it:

### Step 1: Add your API Key
- **Action**: Open the `.env` file in the root folder and add your Gemini API key like this: `GEMINI_API_KEY="your-key-here"`
- **Expectation**: This gives your AI the permission to talk to Google's Gemini servers.

### Step 2: Start the Server
- **Action**: Open your terminal, make sure your virtual environment is active, and run:
  ```bash
  uvicorn app.api.main:app --reload
  ```
- **Expectation**: You will see logs in the terminal saying `Application startup complete`. The server is now running locally on port 8000.

### Step 3: Open the Interactive Documentation
- **Action**: Open your web browser and navigate to: `http://127.0.0.1:8000/docs`
- **Expectation**: You will see a beautiful webpage automatically generated by FastAPI. It shows all the available "endpoints" (URLs you can communicate with).

### Step 4: Chat with the AI!
- **Action**: Click on the `POST /chat` endpoint, click **"Try it out"**, enter a JSON request like `{"query": "Hello! How are you?"}`, and hit **"Execute"**.
- **Expectation**: 
  - The system will process your query. 
  - In the response section on the webpage, you'll see a reply from the `llm_agent`.
  - Try asking a question that makes no sense (like "asdfasdf"), and you'll see the `fallback_agent` respond, safely catching the error!

---

## 📚 Full List of Python Libraries Used

Here is the exact list of libraries we installed (found in `requirements.txt`) and what they do in the background:

- `fastapi`: The web framework used to build our API endpoints.
- `uvicorn`: The lightning-fast server that actually runs our FastAPI code.
- `pydantic`: Validates the data (making sure queries are strings, for instance).
- `pydantic-settings`: Securely loads our secret API keys from the `.env` file.
- `langgraph`: The powerful orchestrator that manages how agents talk to each other.
- `langchain-core`: The base building blocks for chaining AI commands together.
- `langchain_community`: Extra community-built integrations for LangChain.
- `langchain-google-genai`: The specific tool to connect LangChain directly to Google Gemini.
- `chromadb`: The local vector database for storing and searching documents.
- `sentence-transformers`: Converts our English text into mathematical coordinates (embeddings) for ChromaDB to understand.
- `pytest`: Our testing library to automatically verify our code works.
- `httpx`: A tool used behind the scenes (often by FastAPI, LangChain, and our tests) to make web requests.
