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
    slot: datetime
    
class Booking(BaseModel):
    event_id: int
    name: str
    email: EmailStr
    slot: datetime
    
    class Config:
      orm_mode = True
    
    