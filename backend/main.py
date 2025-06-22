from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import sqlalchemy.orm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import func

from models import EventCreate, CreateBooking
from db.database import SessionLocal, engine
from db import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Response models
class SlotResponse(BaseModel):
    id: int
    time: datetime
    event_id: int
    
    class Config:
        orm_mode = True

class EventResponse(BaseModel):
    id: int
    name: str
    description: str
    max_bookings_per_slot: int
    slots: List[SlotResponse] = []
    
    class Config:
        orm_mode = True

class BookingResponse(BaseModel):
    id: int
    event_id: int
    slot_id: int
    name: str
    email: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class SlotResponse(BaseModel):
    id: int
    time: datetime
    event_id: int
    available_slots: int
    is_available: bool
    
    class Config:
        orm_mode = True

@app.post("/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    current_time = datetime.now(datetime.timezone.utc)
    invalid_slots = [ slot.isoformat() for slot in event_data.slots if slot <= current_time ]
    
    if invalid_slots:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Time slots must be in the future. Invalid slots: {', '.join(invalid_slots)}")
    
    # Create event
    db_event = models.Event(
        name=event_data.name,
        description=event_data.description,
        max_bookings_per_slot=event_data.max_bookings_per_slot,
        created_by=event_data.created_by,
        created_at=datetime.utcnow()
    )
    
    # Add slots
    for slot_time in event_data.slots:
        slot = models.Slot(time=slot_time, event=db_event)
        db.add(slot)
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_slot_availability(db: Session, slot_id: int, max_bookings: int) -> tuple[int, bool]:
    """
    Returns a tuple of (available_slots, is_available)
    """
    # Count the number of bookings for this slot
    booked_slots = db.query(func.count(models.Booking.id)).filter(
        models.Booking.slot_id == slot_id
    ).scalar() or 0
    
    available_slots = max(0, max_bookings - booked_slots)
    is_available = available_slots > 0
    
    return available_slots, is_available

@app.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).options(
        sqlalchemy.orm.joinedload(models.Event.slots)
    ).filter(models.Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Add availability info to each slot
    for slot in event.slots:
        available, is_available = get_slot_availability(
            db, slot.id, event.max_bookings_per_slot
        )
        slot.available_slots = available
        slot.is_available = is_available
    
    return event


@app.get("/events", response_model=List[EventResponse])
def list_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()
  
@app.post("/events/{event_id}/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def book_slot(
    event_id: int, 
    booking_data: CreateBooking,
    db: Session = Depends(get_db)
):
    # Check if event exists
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if slot exists for this event
    slot = db.query(models.Slot).filter(
      models.Slot.id == booking_data.slot_id,
      models.Slot.event_id == event_id,
    ).first()
    
    if not slot:
        raise HTTPException(status_code=400, detail="Invalid slot")
    
    current_bookings = db.query(models.Booking).filter(
      models.Booking.slot_id == booking_data.slot_id
    ).count()
    
    if current_bookings >= event.max_bookings_per_slot:
        raise HTTPException(status_code=400, detail="This slot is fully booked")
    
    # Check for existing booking with same email for this slot
    existing_booking = db.query(models.Booking).filter(
      models.Booking.email == booking_data.email,
      models.Booking.slot_id == slot.id
    ).first()
    
    if existing_booking:
        raise HTTPException(status_code=400, detail="You have already booked this slot")
    
    # Check max bookings for this slot
    current_bookings = db.query(models.Booking).filter(
        models.Booking.slot_id == slot.id
    ).count()
    
    if current_bookings >= event.max_bookings_per_slot:
        raise HTTPException(status_code=400, detail="This slot is fully booked")
    
    # Create new booking
    db_booking = models.Booking(
        event_id=event_id,
        slot_id=slot.id,
        name=booking_data.name,
        email=booking_data.email,
        created_at=datetime.utcnow()
    )
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    # Load event with its slots
    event = db.query(models.Event).options(
        sqlalchemy.orm.joinedload(models.Event.slots)
    ).filter(models.Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    return event

@app.get("/events/{event_id}/bookings", response_model=List[BookingResponse])
def get_event_bookings(event_id: int, db: Session = Depends(get_db)):
    # Check if event exists
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return db.query(models.Booking).filter(
        models.Booking.event_id == event_id
    ).all()