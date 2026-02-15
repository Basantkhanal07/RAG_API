# Importing Embeddings model from LangChain_huggingface
from langchain_huggingface import HuggingFaceEmbeddings

# Initializing embeddings model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
