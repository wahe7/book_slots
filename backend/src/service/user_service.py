from sqlalchemy.orm import Session, joinedload

from src.db import models

class UserService:
    def __init__(self, db: Session):
        self.db = db
        
    def get_user_bookings(self, email: str):
        # Use joinedload to fetch related event and slot in a single query
        bookings = self.db.query(models.Booking).options(
            joinedload(models.Booking.event),
            joinedload(models.Booking.slot)
        ).filter(
            models.Booking.email == email
        ).all()

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
