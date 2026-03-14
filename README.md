# 🤖 RAG System With Interview Booking Chatbot

A **FastAPI-based backend** that provides a complete Retrieval-Augmented Generation (RAG) system using a modular, production-ready architecture — featuring document ingestion, multi-turn chat, and an intelligent interview booking flow.

> 🔗 **Live Demo**: [Try the Streamlit App →](https://your-streamlit-demo-link.streamlit.app) *(replace with your actual link)*

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 Document Ingestion | Upload PDF or TXT files, chunk, embed, and store in Pinecone |
| 💬 Conversational RAG | Multi-turn chat with Redis memory and LLM-generated answers |
| 📅 Interview Booking | Book interviews directly through chat (name, email, date, time) |
| 🧠 Semantic Search | Retrieve relevant document chunks via vector similarity |
| 🗃️ Metadata Storage | Track documents and bookings in SQLite |

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes_chat.py          # Chat endpoint
│   │   └── routes_ingest.py        # Document ingestion endpoint
│   ├── core/
│   │   └── config.py               # App configuration
│   ├── db/
│   │   ├── models.py               # SQLAlchemy models
│   │   ├── repositories.py         # DB access layer
│   │   └── session.py              # DB session setup
│   ├── llm/
│   │   ├── embeddings_provider.py  # Google Gemini embeddings
│   │   └── llm_provider.py         # Gemini LLM setup
│   ├── memory/
│   │   └── redis_memory.py         # Redis chat history
│   ├── rag/
│   │   ├── chunking.py             # Fixed & semantic chunking
│   │   └── prompts.py              # Prompt templates
│   ├── services/
│   │   ├── booking_service.py      # Interview booking logic
│   │   ├── ingest_service.py       # Document pipeline
│   │   └── rag_service.py          # RAG pipeline
│   ├── utils/
│   │   ├── pdf_utils.py            # PDF text extraction
│   │   └── text_utils.py           # Text cleaning helpers
│   ├── vectorstore/
│   │   └── pinecone_store.py       # Pinecone integration
│   └── main.py                     # FastAPI app entry point
│
frontend/
├── streamlit_app.py                # Streamlit UI
└── requirements.txt
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🔄 How It Works

### 📥 Document Ingestion Pipeline

```
Upload File → Extract Text → Clean Text → Chunk → Embed → Store in Pinecone + SQLite
```

1. **File Upload** — User uploads a `.pdf` or `.txt` via the Streamlit UI → `POST /api/ingest/upload`
2. **Text Extraction** — PDFs processed with `pdfplumber`; TXT files decoded natively
3. **Text Cleaning** — Removes whitespace artifacts via `clean_text()`
4. **Chunking** — Two strategies available:
   - **Fixed**: Splits into fixed-length segments (`chunk_size=1000`, `overlap=150`)
   - **Semantic**: Splits by paragraphs for more meaningful retrieval
5. **Embedding** — Chunks converted to vectors using `GoogleGenerativeAIEmbeddings`
6. **Vector Storage** — Embeddings + metadata stored in Pinecone via `index.upsert()`
7. **Metadata Storage** — Document info (`id`, `filename`, `chunking`, `created_at`) saved to SQLite

---

### 💬 Chat (RAG) Pipeline

```
User Message → Booking Check → Embed Query → Retrieve Chunks → Build Prompt → LLM → Response
```

1. **Save User Message** — Stored in Redis under `session_id:messages`
2. **Booking Intent Detection** — Checks for keywords like `book`, `schedule`, `appointment`
3. **Query Embedding** — `embeddings.embed_query(message)` converts question to vector
4. **Vector Retrieval** — Pinecone returns top-5 relevant chunks via `index.query(vector, top_k=5)`
5. **Prompt Construction** — Assembles system instructions + chat history + context + question
6. **Response Generation** — Gemini LLM generates the answer via `llm.invoke(prompt)`
7. **Save Response** — Assistant reply stored in Redis for future context

---

### 📅 Interview Booking Flow

When booking intent is detected, the chatbot:

1. Extracts structured data from the message using Gemini
2. Validates required fields: `name`, `email`, `date`, `time`
3. Saves the booking to SQLite (`bookings` table)

```
bookings table: id | session_id | name | email | date | time
```

---

## 🧠 Chat Memory (Redis)

Redis maintains conversation history per session:

```
session_id:messages  →  [role: content, role: content, ...]
```

This enables multi-turn conversations with full context awareness.

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| **FastAPI** | Backend API framework |
| **Streamlit** | Frontend chat & upload UI |
| **Google Gemini** | Embeddings + LLM response generation |
| **Pinecone** | Vector database for similarity search |
| **Redis** | In-memory chat history & session memory |
| **SQLite** | Metadata & booking storage |
| **LangChain** | Wrappers for Gemini, Pinecone, embeddings |
| **pdfplumber** | PDF text extraction |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Redis running locally or via cloud
- Pinecone account & API key
- Google Gemini API key

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in `/backend`:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_index_name
REDIS_URL=redis://localhost:6379
```

### Run the App

```bash
# Start the FastAPI backend
cd backend
uvicorn app.main:app --reload

# Start the Streamlit frontend (in a new terminal)
cd frontend
streamlit run streamlit_app.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/ingest/upload` | Upload and ingest a document |
| `POST` | `/api/chat/message` | Send a chat message |

---



