import redis
from typing import List, Dict
from app.core.config import settings

# Connect to Redis using URL from settings
# decode_responses=True ensures strings instead of bytes
r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


# Function to save a chat message to Redis

def save_message(session_id: str, role: str, content: str):
    r.rpush(f"{session_id}:messages", f"{role}:{content}")  # add ":messages"

# Function to get chat history from Redis
def get_history(session_id: str, limit: int = 10) -> List[Dict]:
    msgs = r.lrange(f"{session_id}:messages", -limit, -1)  # use same key
    history = []
    for m in msgs:
        role, content = m.split(":", 1)
        history.append({"role": role, "content": content})
    return history

