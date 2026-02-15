import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://localhost:8000/api"

# App title and session ID

st.title("RAG System With Interview Booking Chatbot")

session_id = st.text_input("Session ID", value="user1")

# Document Ingestion Section
st.header("1. Upload Document")
chunking = st.selectbox("Chunking Strategy", ["fixed", "semantic"])
uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

if st.button("Upload") and uploaded_file:
    files = {"file": uploaded_file}
    data = {"chunking": chunking}
    res = requests.post(f"{BACKEND_URL}/ingest/upload", files=files, data=data)
    st.json(res.json())

# Chat Section
st.header("2. Chat")
query = st.text_input("Ask something")

if st.button("Send") and query:
    payload = {"session_id": session_id, "message": query}
    res = requests.post(f"{BACKEND_URL}/chat/query", json=payload)
    st.json(res.json())
