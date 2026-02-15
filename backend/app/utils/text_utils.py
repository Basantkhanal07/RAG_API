# Function to clean and normalize text

def clean_text(text: str) -> str:
    return " ".join(text.split())
