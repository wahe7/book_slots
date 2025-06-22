from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .slot import SlotResponse

class EventBase(BaseModel):
    name: str
    description: str
    max_bookings_per_slot: int = Field(..., gt=0, description="Maximum number of bookings allowed per slot")

class EventCreate(EventBase):
    slots: List[datetime]
    created_by: str

class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    max_bookings_per_slot: Optional[int] = Field(None, gt=0)
    
class EventResponse(EventBase):
    id: int
    created_by: str
    created_at: datetime
    slots: List[SlotResponse] = []
    
    class Config:
        orm_mode = True
        
    @classmethod
    def from_orm(cls, obj):
        # Handle both ORM model and dictionary
        if isinstance(obj, dict):
            return cls(**obj)
        return super().from_orm(obj)
        
# Alias for backward compatibility
Event = EventResponse