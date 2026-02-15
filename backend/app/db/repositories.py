from sqlalchemy.orm import Session
from app.db.models import Document, Booking

# Function to save an uploaded document to the database
def save_document(db: Session, filename: str, chunking: str) -> Document:
    doc = Document(filename=filename, chunking=chunking)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

# Function to save a booking to the database
def save_booking(db: Session, session_id: str, name: str, email: str, date: str, time: str) -> Booking:
    booking = Booking(session_id=session_id, name=name, email=email, date=date, time=time)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
