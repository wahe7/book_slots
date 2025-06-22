from pydantic import BaseModel
from datetime import datetime

class CreateBooking(BaseModel):
    name: str
    email: str
    slot_id: int

    class Config:
        orm_mode = True
 

class BookingResponse(CreateBooking):
    id: int
    event_id: int
    slot_id: int
    name: str
    email: str
    created_at: datetime
    event_name: str
    slot_time: str 

    class Config:
        orm_mode = True