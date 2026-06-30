from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

    APP_NAME: str = "RAG Backend"
    ENV: str = "dev"
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:8501"
    CORS_ORIGINS: str = ""

    # Google Gemini API settings
    GOOGLE_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Pinecone for vector database
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str = "rag-api"
    PINECONE_ENVIRONMENT: str = "us-east-1"

    # Database settings for storing chat/booking info
    # SQLite
    DATABASE_URL: str = "sqlite:///./rag.db"

    # Redis for session storage
    REDIS_URL: str = "redis://localhost:6379/0"

    @property
    def allowed_origins(self) -> list[str]:
        configured_origins = [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]
        default_origins = [
            self.FRONTEND_URL,
            "http://localhost:8501",
            "http://localhost:3000",
            "http://127.0.0.1:8501",
            "http://127.0.0.1:3000",
        ]
        return list(dict.fromkeys(configured_origins + default_origins))

settings = Settings()
