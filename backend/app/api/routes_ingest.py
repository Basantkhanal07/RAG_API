from fastapi import APIRouter, UploadFile, File, Form
from app.services.ingest_service import ingest_document

# Create a router for ingestion-related endpoints
router = APIRouter()

# Endpoint to upload a document and ingest it into the system
@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    chunking: str = Form("fixed"),  # fixed | semantic
):
    return await ingest_document(file, chunking)
