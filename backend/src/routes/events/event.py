from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.db.database import get_db
from src.schemas.event import EventCreate, EventUpdate, EventResponse
from src.service.event_service import EventService
from src.service.booking_service import BookingService
from src.schemas.booking import CreateBooking, BookingResponse

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db)
):
    return EventService(db).create_event(event_data)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event_service = EventService(db)
    event = event_service.get_event(event_id)
    
    # The event_service.get_event() now returns a dictionary with slots
    # that already include availability information
    return event


@router.get("/", response_model=List[EventResponse])
def list_events(
    db: Session = Depends(get_db)
):
    return EventService(db).get_events()


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    db: Session = Depends(get_db)
):
    return EventService(db).update_event(event_id, event_data)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    EventService(db).delete_event(event_id)
    return {"message": "Event deleted successfully"}


@router.post("/{event_id}/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def book_slot(
    event_id: int,
    booking_data: CreateBooking,
    db: Session = Depends(get_db)
):
    return BookingService(db).create_booking(event_id, booking_data)


@router.get("/{event_id}/bookings", response_model=List[BookingResponse])
def get_event_bookings(
    event_id: int,
    db: Session = Depends(get_db)
):
    return BookingService(db).get_event_bookings(event_id)


@router.get("/user/{email}/bookings", response_model=List[BookingResponse])
def get_user_bookings(
    email: str,
    db: Session = Depends(get_db)
):
    return BookingService(db).get_user_bookings(email)
