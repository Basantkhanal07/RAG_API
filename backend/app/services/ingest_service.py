from typing import List
import os
import io
from dotenv import load_dotenv

import pdfplumber
from app.llm.embeddings_provider import embeddings
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from app.rag.chunking import fixed_chunking, semantic_chunking

# Import DB session and repository to save documents
from app.db.session import SessionLocal
from app.db.repositories import save_document

# Load environment variables
load_dotenv()

# Pinecone config
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rag-api")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

if not PINECONE_API_KEY:
    raise ValueError("Pinecone API key not set! Please set PINECONE_API_KEY in your environment.")


async def ingest_document(file, chunking_strategy: str = "fixed"):
    """
    Ingest a document (PDF or TXT):
    1) Read file content
    2) Extract text (proper PDF parsing)
    3) Split into chunks
    4) Convert to Document objects with metadata
    5) Store embeddings in Pinecone
    6) Save document info in SQLite
    """

    filename = getattr(file, "filename", "unknown_file")

    # Read the file content
    contents = await file.read()

    # Extract text
    text = ""
    if filename.lower().endswith(".pdf"):
        try:
            with pdfplumber.open(io.BytesIO(contents)) as pdf:
                pages_text = [page.extract_text() or "" for page in pdf.pages]
                text = "\n\n".join(pages_text)
        except Exception as e:
            return {"error": f"Failed to read PDF file: {str(e)}"}
    elif filename.lower().endswith(".txt"):
        try:
            text = contents.decode("utf-8", errors="ignore")
        except Exception as e:
            return {"error": f"Failed to decode TXT file: {str(e)}"}
    else:
        return {"error": f"Unsupported file type: {filename}"}

    if not text.strip():
        return {"error": "No text extracted from the document."}

    # Split into chunks
    if chunking_strategy == "fixed":
        chunks: List[str] = fixed_chunking(text, chunk_size=500, overlap=50)
    elif chunking_strategy == "semantic":
        chunks: List[str] = semantic_chunking(text, max_size=1200)
    else:
        chunks: List[str] = [text]

    # Convert chunks to Document objects with metadata for Pinecone
    docs: List[Document] = [
        Document(page_content=chunk, metadata={"filename": filename})
        for chunk in chunks
    ]

    # Store embeddings in Pinecone
    try:
        vectorstore = PineconeVectorStore.from_documents(
            docs,
            embeddings,
            index_name=PINECONE_INDEX_NAME,
        )
    except Exception as e:
        return {"error": f"Failed to store embeddings in Pinecone: {str(e)}"}

    # SAVE DOCUMENT TO SQLITE
    
    try:
        db = SessionLocal()
        doc_row = save_document(db, filename=filename, chunking=chunking_strategy)
        db.close()
    except Exception as e:
        return {"error": f"Stored in Pinecone but failed to save in SQLite: {str(e)}"}

    return {
        "message": f"{len(docs)} chunks stored in Pinecone index '{PINECONE_INDEX_NAME}'",
        "chunks": len(docs),
        "filename": filename,
        "document_id": doc_row.id,   # Return the saved document ID
    }
