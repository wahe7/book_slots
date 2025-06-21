from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from pydantic import BaseModel

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
class EventResponse(BaseModel):
    id: int
    name: str
    description: str
    max_bookings_per_slot: int
    
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

@app.post("/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    # Create event
    db_event = models.Event(
        name=event_data.name,
        description=event_data.description,
        max_bookings_per_slot=event_data.max_bookings_per_slot
    )
    
    # Add slots
    for slot_time in event_data.slots:
        slot = models.Slot(time=slot_time, event=db_event)
        db.add(slot)
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

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
        models.Slot.event_id == event_id,
        models.Slot.time == booking_data.slot
    ).first()
    
    if not slot:
        raise HTTPException(status_code=400, detail="Invalid slot")
    
    # Check for existing booking with same email for this slot
    existing_booking = db.query(models.Booking).filter(
        models.Booking.event_id == event_id,
        models.Booking.slot_id == slot.id,
        models.Booking.email == booking_data.email
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
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
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