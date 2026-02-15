from fastapi import FastAPI
from dotenv import load_dotenv

from app.core.config import settings
from app.api.routes_ingest import router as ingest_router
from app.api.routes_chat import router as chat_router

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app instance
app = FastAPI(title=settings.APP_NAME)

# Register ingestion routes
app.include_router(ingest_router, prefix="/api/ingest", tags=["Ingestion"])

# Register chat routes
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])

# Default endpoint to check if server is running
@app.get("/")
def home():
    return {"message": "API is running successfully"}


