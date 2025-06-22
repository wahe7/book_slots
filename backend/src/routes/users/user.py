from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.db.database import get_db
from src.schemas.booking import BookingResponse
from src.service.user_service import UserService

router = APIRouter(tags=["users"])

@router.get("/{email}/bookings", response_model=List[BookingResponse])
def get_user_bookings(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Get all bookings for a specific user by email
    
    - **email**: The email address of the user
    """
    user_service = UserClass(db)
    try:
        return user_service.get_user_bookings(email)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching bookings: {str(e)}"
        )

@router.get("/{email}/bookings/{booking_id}", response_model=BookingResponse)
def get_user_booking(
    email: str,
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific booking for a user
    
    - **email**: The email address of the user
    - **booking_id**: The ID of the booking to retrieve
    """
    user_service = UserClass(db)
    try:
        bookings = user_service.get_user_bookings(email, db)
        booking = next((b for b in bookings if b["id"] == booking_id), None)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found for this user"
            )
        return booking
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the booking: {str(e)}"
        )

@router.delete("/{email}/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_user_booking(
    email: str,
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Cancel a specific booking for a user
    
    - **email**: The email address of the user
    - **booking_id**: The ID of the booking to cancel
    """
    from ...service.booking_service import BookingService
    
    # First verify the booking belongs to this user
    user_service = UserClass(db)
    try:
        bookings = user_service.get_user_bookings(email, db)
        if not any(b["id"] == booking_id for b in bookings):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found for this user"
            )
        
        # If booking exists and belongs to user, cancel it
        booking_service = BookingService(db)
        booking_service.cancel_booking(booking_id)
        return {"message": "Booking cancelled successfully"}
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while cancelling the booking: {str(e)}"
        )