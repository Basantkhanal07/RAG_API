# RAG System With Interview Booking Chatbot

This is a FastAPI-based backend project that provides a complete Retrieval-Augmented Generation (RAG) system using a modular and industry-standard architecture.

It includes two main REST APIs:

## 1) Document Ingestion API
- Upload `.pdf` or `.txt` documents
- Extract text from files
- Apply selectable chunking strategies (fixed / semantic)
- Generate embeddings using an LLM embedding model
- Store embeddings in a vector database Pinecone
- Save document metadata in a database

## 2) Conversational RAG API
- Custom RAG implementation (no RetrievalQAChain)
- Multi-turn chat support
- Redis-based chat memory
- Retrieves relevant chunks from the vector database
- Generates final answers using the LLM with retrieved context
- Supports interview booking through chat (name, email, date, time)
- Stores booking information in a database
