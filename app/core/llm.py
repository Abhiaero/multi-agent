from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

def get_llm(temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """
    Initializes and returns the Gemini Pro LLM wrapper.
    """
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    # Using Gemini 1.5 Pro as requested (the current default/latest pro model in API)
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=temperature,
        google_api_key=settings.gemini_api_key,
        convert_system_message_to_human=True
    )
