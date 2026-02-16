from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "RAG Backend"
    ENV: str = "dev"

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

settings = Settings()
