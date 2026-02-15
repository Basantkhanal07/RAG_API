from typing import List, Dict, Any
from pinecone import Pinecone
from app.core.config import settings

# Initialize Pinecone 
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Connect to the index
index = pc.Index(settings.PINECONE_INDEX_NAME)

#  Function to upsert (add/update) vectors in Pinecone
def upsert_vectors(vectors: List[Dict[str, Any]]):
    index.upsert(vectors=vectors)

# Function to # Query vectors from Pinecone
def query_vectors(vector: List[float], top_k: int = 5):
    return index.query(vector=vector, top_k=top_k, include_metadata=True)
