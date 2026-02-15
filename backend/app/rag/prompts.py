SYSTEM_PROMPT = """
You are a helpful assistant.
Answer using the provided context only.
If the answer is not in the context, say This is not in the file.
"""

BOOKING_PROMPT = """
Extract interview booking details from the user message.

Return JSON with keys:
name, email, date, time

If missing, return empty string for that field.
"""
