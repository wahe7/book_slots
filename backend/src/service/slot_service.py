from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.db import models
from src.schemas.slot import SlotCreate

class SlotService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_slot(self, slot_data: SlotCreate):
        slot = models.Slot(time=slot_data.time, event_id=slot_data.event_id)
        self.db.add(slot)
        self.db.commit()
        self.db.refresh(slot)
        return slot
    
    def get_slot(self, slot_id: int):
        slot = self.db.query(models.Slot).filter(models.Slot.id == slot_id).first()
        if not slot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
        return slot
    
    def get_slots(self):
        return self.db.query(models.Slot).all()
