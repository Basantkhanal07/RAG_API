from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
import json
import re

from app.llm.embeddings_provider import embeddings
from app.llm.llm_provider import llm
from app.vectorstore.pinecone_store import query_vectors
from app.memory.redis_memory import save_message, get_history
from app.rag.prompts import SYSTEM_PROMPT, BOOKING_PROMPT
from app.services.booking_service import store_booking


def _strip_code_fences(text: str) -> str:
   # Removes markdown code fences (```json ... ```) from LLM output.
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
        t = re.sub(r"\n?```$", "", t)
    return t.strip()


def _safe_json_loads(text: str) -> Optional[Dict[str, Any]]:
    # Safely parse JSON from LLM output.
    cleaned = _strip_code_fences(text)

    # 1) direct parse
    try:
        obj = json.loads(cleaned)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

     # Try to extract first JSON object in text
    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if match:
        candidate = match.group(0).strip()
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                return obj
        except Exception:
            return None

    return None

# Defining Simple rule-based detection of booking intent
def _is_booking_intent(message: str) -> bool:
    msg = message.lower()
    keywords = [
        "book",
        "booking",
        "schedule",
        "interview",
        "appointment",
        "meeting",
        "call",
        "slot",
    ]
    return any(k in msg for k in keywords)


def _normalize_booking_fields(data: Dict[str, Any]) -> Dict[str, str]:
    # Ensure all fields are strings and strip whitespace
    return {
        "name": str(data.get("name", "")).strip(),
        "email": str(data.get("email", "")).strip(),
        "date": str(data.get("date", "")).strip(),
        "time": str(data.get("time", "")).strip(),
    }


def _is_complete_booking(data: Dict[str, str]) -> bool:
    return all(data.get(k) for k in ["name", "email", "date", "time"])


def _format_history_for_prompt(history: List[Dict[str, str]]) -> str:
    
    # Converts redis history to clean text for the prompt.
    lines: List[str] = []
    for h in history:
        role = h.get("role", "user")
        content = h.get("content", "")
        lines.append(f"{role.upper()}: {content}")
    return "\n".join(lines).strip()

# Main RAG Chat Function
async def chat_rag(session_id: str, message: str) -> Dict[str, Any]:
    """
    Flow:
    1) Save user msg to Redis
    2) Detect booking intent and extract booking fields via Gemini
    3) If booking complete -> store in SQLite
    4) Else -> run RAG:
        - embed query
        - retrieve top_k docs from Pinecone
        - create context
        - ask Gemini with context + history
    5) Save assistant response to Redis
    """

    # 1) Save user message
    save_message(session_id, "user", message)

    # Load recent history
    history = get_history(session_id=session_id, limit=12)
    history_text = _format_history_for_prompt(history)

    # 2) Booking intent
    if _is_booking_intent(message):
        booking_prompt = f"""{BOOKING_PROMPT}

Chat History:
{history_text}

User message:
{message}

Return ONLY valid JSON.
"""

        booking_raw = llm.invoke(booking_prompt).content
        booking_data = _safe_json_loads(booking_raw)

        if booking_data:
            normalized = _normalize_booking_fields(booking_data)

            if _is_complete_booking(normalized):
                booking = store_booking(session_id=session_id, data=normalized)

                assistant_msg = (
                    f"Interview booked successfully!\n\n"
                    f"Name: {normalized['name']}\n"
                    f"Email: {normalized['email']}\n"
                    f"Date: {normalized['date']}\n"
                    f"Time: {normalized['time']}"
                )

                save_message(session_id, "assistant", assistant_msg)

                return {
                    "answer": assistant_msg,
                    "intent": "booking",
                    "booking_id": booking.id,
                    "booking": normalized,
                }

            # Booking intent but missing fields
            missing = [k for k in ["name", "email", "date", "time"] if not normalized.get(k)]
            ask_msg = (
                "I can book your interview but I still need:\n"
                + "\n".join([f"- {m}" for m in missing])
            )

            save_message(session_id, "assistant", ask_msg)
            return {
                "answer": ask_msg,
                "intent": "booking",
                "missing_fields": missing,
                "booking_partial": normalized,
            }

        # If LLM failed to parse JSON
        fail_msg = (
            "I think you want to book an interview, but I couldn't extract the details.\n"
            "Please send like:\n"
            "`My name is X, email is Y, date is 2026-02-15, time is 3:00 PM`"
        )
        save_message(session_id, "assistant", fail_msg)
        return {"answer": fail_msg, "intent": "booking"}

    # 3) Normal RAG flow

    # Embed query
    query_vector = embeddings.embed_query(message)

    # Retrieve top matches from Pinecone
    results = query_vectors(query_vector, top_k=5)
    matches = results.get("matches", [])

    # Build context for LLM
    context_chunks: List[str] = []
    sources: List[str] = []

    for m in matches:
        meta = m.get("metadata", {}) or {}
        chunk_text = meta.get("text", "")
        filename = meta.get("filename", "unknown")

        if chunk_text:
            context_chunks.append(chunk_text)
        sources.append(filename)

    context = "\n\n---\n\n".join(context_chunks).strip()

    # Create final prompt
    final_prompt = f"""{SYSTEM_PROMPT}

Chat History:
{history_text}

Context:
{context}

User Question:
{message}
"""
    # Get assistant answer
    answer = llm.invoke(final_prompt).content.strip()

    # Save assistant response
    save_message(session_id, "assistant", answer)

    # Remove duplicates sources
    sources_unique = list(dict.fromkeys(sources))

    return {
        "answer": answer,
        "intent": "rag",
        "sources": sources_unique,
        "top_k": len(matches),
    }
