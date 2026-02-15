from typing import List

# Function to split text into fixed-size chunks
def fixed_chunking(text: str, chunk_size: int = 1000, overlap: int = 150) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# Function to split text into semantic chunks 
def semantic_chunking(text: str, max_size: int = 1200) -> List[str]:
    
    # Split text into paragraphs and remove empty ones
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    buffer = ""

    for p in paragraphs:
        if len(buffer) + len(p) < max_size:
            buffer += " " + p
        else:
            chunks.append(buffer.strip())
            buffer = p

    if buffer.strip():
        chunks.append(buffer.strip())

    return chunks
