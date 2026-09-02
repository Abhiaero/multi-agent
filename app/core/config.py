from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str = Field(default="", description="Google Gemini API Key")
    
    # App Settings
    app_name: str = "Multi-Agent AI Platform"
    debug: bool = False
    
    # RAG Settings
    chroma_db_dir: str = "./chroma_db"
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Evaluator Settings
    metrics_db_path: str = "./metrics.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
