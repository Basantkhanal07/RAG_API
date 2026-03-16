# Importing Embeddings model from LangChain_huggingface
from langchain_huggingface import HuggingFaceEmbeddings

# Initializing embeddings model
embeddings = HuggingFaceEmbeddings(model_name="all-MPNet-base-v2")
