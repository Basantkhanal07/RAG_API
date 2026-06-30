from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import traceback

from app.services.rag_service import chat_rag

# Create a router for chat-related endpoints
router = APIRouter()

# Request model
class ChatRequest(BaseModel):
    message: str
    session_id: str

    class Config:
        extra = "ignore"  # ignore extra fields to avoid 422

# Response model (generic dict)
class ChatResponse(BaseModel):
    answer: str
    intent: str
    booking_id: str | None = None  # <-- change to str
    booking: Dict[str, str] | None = None
    missing_fields: list[str] | None = None
    sources: list[str] | None = None
    top_k: int | None = None


# Main chat endpoint It sends the user message + session_id to the RAG service and returns the final response

@router.post("/query", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        res: dict[str, Any] = await chat_rag(req.session_id, req.message)
        return res
    except Exception as e:
        # Catch all exceptions to prevent 500 HTML response
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Backend error: {str(e)}")
