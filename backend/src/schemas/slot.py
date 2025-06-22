from pydantic import BaseModel
from datetime import datetime

class SlotCreate(BaseModel):
    time: datetime
    event_id: int

class SlotResponse(BaseModel):
    id: int
    time: datetime
    event_id: int
    available_slots: int
    max_slots: int

    class Config:
        orm_mode = True
