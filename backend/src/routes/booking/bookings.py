from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.db.database import get_db
from src.schemas.booking import CreateBooking, BookingResponse
from src.service.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: CreateBooking,
    db: Session = Depends(get_db)
):
    """
    Create a new booking for a slot
    
    - **name**: Name of the person making the booking
    - **email**: Email of the person (must be unique per slot)
    - **slot_id**: ID of the slot to book
    """
    booking_service = BookingService(db)
    try:
        return booking_service.create_booking(booking_data.slot_id, booking_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the booking"
        )

@router.get("/event/{event_id}", response_model=List[BookingResponse])
def get_event_bookings(
    event_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all bookings for a specific event
    """
    booking_service = BookingService(db)
    try:
        return booking_service.get_event_bookings(event_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching bookings"
        )

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific booking by ID
    """
    booking_service = BookingService(db)
    booking = booking_service.get_booking(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Cancel a booking by ID
    """
    booking_service = BookingService(db)
    try:
        booking_service.cancel_booking(booking_id)
        return {"message": "Booking cancelled successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while cancelling the booking"
        )
