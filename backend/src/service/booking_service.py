from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from src.db import models

class BookingService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_bookings(self, email: str):
        bookings = self.db.query(models.Booking).options(
            joinedload(models.Booking.event),
            joinedload(models.Booking.slot)
        ).filter(models.Booking.email == email).all()

        result = []
        for booking in bookings:
            result.append({
                "id": booking.id,
                "event_id": booking.event_id,
                "slot_id": booking.slot_id,
                "name": booking.name,
                "email": booking.email,
                "created_at": booking.created_at,
                "event_name": booking.event.name if booking.event else None,
                "slot_time": booking.slot.time.isoformat() if booking.slot else None
            })

        return result
        
    def _send_booking_confirmation(self, booking, event, slot):
        """
        Send booking confirmation email to the user using EmailService
        """
        from src.service.email_service import EmailService
        
        # Format the date and time in a user-friendly way
        slot_time = slot.time.strftime("%A, %B %d, %Y at %I:%M %p")
        
        # Use the EmailService's booking confirmation method
        EmailService.send_booking_confirmation(
            to_email=booking.email,
            name=booking.name,
            event_name=event.name,
            slot_time=slot_time,
            booking_id=booking.id
        )

    def create_booking(self, event_id: int, booking_data):
        """
        Create a new booking for an event slot and send confirmation email
        """
        from datetime import datetime
        from sqlalchemy.exc import IntegrityError
        
        try:
            # Check if slot exists and get the event
            slot = self.db.query(models.Slot).options(
                joinedload(models.Slot.event)
            ).filter(
                models.Slot.id == booking_data.slot_id,
                models.Slot.event_id == event_id
            ).first()
            
            if not slot:
                error_msg = f"Slot {booking_data.slot_id} not found for event {event_id}"
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"detail": error_msg}
                )
                
            # Get the event to check max bookings
            event = slot.event
            
            # Check if slot is already booked by this email
            existing_booking = self.db.query(models.Booking).filter(
                models.Booking.slot_id == booking_data.slot_id,
                models.Booking.email == booking_data.email
            ).first()
            
            if existing_booking:
                error_msg = f"You have already booked this slot"
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "detail": "Booking failed",
                        "error": error_msg
                    }
                )
                
            # Check if slot is full
            booking_count = self.db.query(models.Booking).filter(
                models.Booking.slot_id == booking_data.slot_id
            ).count()
            
            if booking_count >= event.max_bookings_per_slot:
                error_msg = "This slot is already fully booked"
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "detail": "Booking failed",
                        "error": error_msg
                    }
                )
                
            # Create the booking
            booking = models.Booking(
                event_id=event_id,
                slot_id=booking_data.slot_id,
                name=booking_data.name,
                email=booking_data.email,
                created_at=datetime.utcnow()
            )
            
            try:
                self.db.add(booking)
                self.db.commit()
                self.db.refresh(booking)
                
                # Send confirmation email
                try:
                    self._send_booking_confirmation(booking, event, slot)
                except Exception:
                    # Don't fail the booking if email sending fails
                    pass
                
                # Return the booking with related data
                return {
                    "id": booking.id,
                    "event_id": booking.event_id,
                    "slot_id": booking.slot_id,
                    "name": booking.name,
                    "email": booking.email,
                    "created_at": booking.created_at,
                    "event_name": event.name,
                    "slot_time": slot.time.isoformat()
                }
                
            except Exception:
                self.db.rollback()
                raise
            
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "detail": "Booking failed",
                    "error": "This slot is no longer available. Please try another slot."
                }
            )
        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "detail": "Booking failed",
                    "error": "An unexpected error occurred while processing your booking"
                }
            )