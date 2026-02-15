from typing import Dict
from app.db.session import SessionLocal
from app.db.repositories import save_booking

# function to store booking information in the database
def store_booking(session_id: str, data: Dict):
    db = SessionLocal()
    booking = save_booking(
        db,
        session_id=session_id,
        name=data["name"],
        email=data["email"],
        date=data["date"],
        time=data["time"],
    )
    db.close()
    return booking
