# Importing Embeddings model from LangChain
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# Initializing embeddings model
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
