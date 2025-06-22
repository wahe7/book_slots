from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

class EventCreate(BaseModel):
    name: str
    description: str
    slots: List[datetime]
    max_bookings_per_slot: int
    created_by: str
    
class Event(EventCreate):
    id: int
    name: str
    description: str
    slots: List[datetime] = []
    max_bookings_per_slot: int
    created_by: str
    created_at: datetime = None
    
    class Config:
        orm_mode = True

class CreateBooking(BaseModel):
    name: str
    email: EmailStr
    slot_id: int
    
class Booking(BaseModel):
    event_id: int
    name: str
    email: EmailStr
    slot_id: int    
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
      
class BookingResponse(Booking):
    slot: SlotResponse

    class Config:
        orm_mode = True
    