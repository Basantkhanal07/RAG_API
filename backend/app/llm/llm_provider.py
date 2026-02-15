# Importing Google Gemini chat model from LangChain
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

# Initializing LLM object for chat generation
llm = ChatGoogleGenerativeAI(
    model=settings.GEMINI_MODEL,  # "gemini-2.5-flash"
    temperature=0.2,
    api_key=settings.GOOGLE_API_KEY
)
