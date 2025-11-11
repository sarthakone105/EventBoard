from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import Event
from schemas import EventCreate, EventUpdate, EventOut
from utils.crud_helpers import create_object, update_object, delete_object

router = APIRouter(prefix="/events", tags=["Events"])


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Event ✅
@router.post("", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    return create_object(db, Event, payload, label="Event")


# Get All Events ✅
@router.get("", response_model=List[EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


# Get Single Event ✅
@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Event not found")
    return event


# Update Event ✅
@router.patch("/{event_id}", response_model=EventOut)
def update_event(event_id: int, payload: EventUpdate, db: Session = Depends(get_db)):
    return update_object(db, Event, "event_id", event_id, payload, "Event")


# Delete Event ✅
@router.delete("/{event_id}", status_code=status.HTTP_200_OK)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    return delete_object(db, Event, "event_id", event_id, "Event")
