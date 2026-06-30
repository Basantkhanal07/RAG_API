import redis
from typing import List, Dict
from app.core.config import settings

# Connect to Redis using URL from settings
# decode_responses=True ensures strings instead of bytes
r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
_memory_fallback: dict[str, list[str]] = {}


# Function to save a chat message to Redis

def save_message(session_id: str, role: str, content: str):
    key = f"{session_id}:messages"
    message = f"{role}:{content}"
    try:
        r.rpush(key, message)
    except redis.RedisError:
        _memory_fallback.setdefault(key, []).append(message)

# Function to get chat history from Redis
def get_history(session_id: str, limit: int = 10) -> List[Dict]:
    key = f"{session_id}:messages"
    try:
        msgs = r.lrange(key, -limit, -1)
    except redis.RedisError:
        msgs = _memory_fallback.get(key, [])[-limit:]

    history = []
    for m in msgs:
        role, content = m.split(":", 1)
        history.append({"role": role, "content": content})
    return history

