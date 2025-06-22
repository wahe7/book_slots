from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.db import models
from src.schemas.event import EventCreate, EventUpdate

class EventService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_event(self, event_data: EventCreate):
        current_time = datetime.now(timezone.utc)
        
        # Validate required fields
        if not event_data.name or not event_data.name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"detail": "Event name is required"}
            )
            
        if not event_data.slots:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"detail": "At least one time slot is required"}
            )
        
        # Convert string timestamps to datetime objects if needed
        processed_slots = []
        for slot in event_data.slots:
            if isinstance(slot, str):
                try:
                    # Handle both with and without timezone
                    if 'Z' in slot:
                        slot_dt = datetime.fromisoformat(slot.replace('Z', '+00:00'))
                    else:
                        slot_dt = datetime.fromisoformat(slot)
                        # If no timezone info, assume it's in UTC
                        if slot_dt.tzinfo is None:
                            slot_dt = slot_dt.replace(tzinfo=timezone.utc)
                    processed_slots.append(slot_dt)
                except (ValueError, AttributeError) as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "detail": f"Invalid datetime format: {slot}",
                            "invalid_format": slot
                        }
                    )
            else:
                processed_slots.append(slot)
        
        # Sort slots chronologically
        processed_slots.sort()
        
        # Validate slots are in the future and not duplicated
        invalid_slots = []
        seen_slots = set()
        
        for slot in processed_slots:
            slot_iso = slot.isoformat()
            if slot_iso in seen_slots:
                invalid_slots.append({"time": slot_iso, "error": "Duplicate time slot"})
            elif slot <= current_time:
                invalid_slots.append({"time": slot_iso, "error": "Time slot is in the past"})
            seen_slots.add(slot_iso)
        
        if invalid_slots:
            error_detail = {
                "detail": "One or more time slots are invalid",
                "errors": {
                    "slots": invalid_slots
                }
            }
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_detail
            )
        
        try:
            # Create event
            db_event = models.Event(
                name=event_data.name.strip(),
                description=event_data.description.strip() if event_data.description else None,
                max_bookings_per_slot=event_data.max_bookings_per_slot,
                created_by=event_data.created_by.strip(),
                created_at=datetime.now(timezone.utc)
            )
            
            # Add slots in a single batch
            self.db.add_all([
                models.Slot(time=slot_time, event=db_event)
                for slot_time in processed_slots
            ])
            
            self.db.add(db_event)
            self.db.commit()
            self.db.refresh(db_event)
            
            # Return the created event with its slots using get_event for proper serialization
            return self.get_event(db_event.id)
            
        except Exception as e:
            self.db.rollback()
            # Log the full error for debugging
            import logging
            logging.error(f"Error creating event: {str(e)}", exc_info=True)
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"detail": "An error occurred while creating the event. Please try again later."}
            )
    
    def get_event(self, event_id: int):
        from sqlalchemy.orm import joinedload
        
        # Get the event with its slots
        event = self.db.query(models.Event)\
            .options(joinedload(models.Event.slots))\
            .filter(models.Event.id == event_id)\
            .first()
            
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
            
        # Convert to dict to add computed fields
        event_dict = {
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "created_by": event.created_by,
            "max_bookings_per_slot": event.max_bookings_per_slot,
            "created_at": event.created_at,
            "slots": []
        }
        
        # Add slot availability information
        for slot in event.slots:
            available, _ = self.get_slot_availability(slot.id, event.max_bookings_per_slot)
            # Ensure we're creating a new dictionary with all required fields
            slot_dict = {
                "id": slot.id,
                "time": slot.time,
                "event_id": slot.event_id,
                "available_slots": available,
                "max_slots": event.max_bookings_per_slot
            }
            event_dict["slots"].append(slot_dict)
            
        # Convert to a plain dictionary to ensure no SQLAlchemy models remain
        return dict(event_dict)
    
    def get_events(self):
        from sqlalchemy.orm import joinedload
        
        # Get all events with their slots
        events = self.db.query(models.Event)\
            .options(joinedload(models.Event.slots))\
            .all()
            
        result = []
        for event in events:
            # Convert to dict to add computed fields
            event_dict = {
                "id": event.id,
                "name": event.name,
                "description": event.description,
                "created_by": event.created_by,
                "max_bookings_per_slot": event.max_bookings_per_slot,
                "created_at": event.created_at,
                "slots": []
            }
            
            # Add slot availability information
            for slot in event.slots:
                available, _ = self.get_slot_availability(slot.id, event.max_bookings_per_slot)
                slot_dict = {
                    "id": slot.id,
                    "time": slot.time,
                    "event_id": slot.event_id,
                    "available_slots": available,
                    "max_slots": event.max_bookings_per_slot
                }
                event_dict["slots"].append(slot_dict)
                
            # Convert to a plain dictionary to ensure no SQLAlchemy models remain
            result.append(dict(event_dict))
            
        return result
        
    def get_slot_availability(self, slot_id: int, max_bookings: int):
        """
        Check how many slots are available for a given slot ID
        Returns a tuple of (available_slots, is_available)
        """
        from sqlalchemy import func
        
        # Get total bookings for this slot
        booking_count = self.db.query(func.count(models.Booking.id))\
            .filter(models.Booking.slot_id == slot_id)\
            .scalar() or 0
            
        available = max(0, max_bookings - booking_count)
        is_available = available > 0
        
        return available, is_available
    
    def update_event(self, event_id: int, event_data: EventCreate):
        
        available = max(0, max_bookings - booking_count)
        is_available = available > 0
        
        # Add slot information
        for slot in event.slots:
            available, _ = self.get_slot_availability(slot.id, event.max_bookings_per_slot)
            event_dict["slots"].append({
                "id": slot.id,
                "time": slot.time,
                "event_id": slot.event_id,
                "available_slots": available,
                "max_slots": event.max_bookings_per_slot
            })
            
        return event_dict
    
    def delete_event(self, event_id: int):
        event = self.db.query(models.Event).filter(models.Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        self.db.delete(event)
        self.db.commit()
        return event