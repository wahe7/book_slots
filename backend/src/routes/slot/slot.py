from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.db.database import get_db
from src.schemas.slot import SlotCreate, SlotResponse
from src.service.slot_service import SlotService

router = APIRouter(prefix="/slots", tags=["slots"])

@router.post("/", response_model=SlotResponse, status_code=status.HTTP_201_CREATED)
def create_slot(
    slot_data: SlotCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new slot for an event
    
    - **time**: The date and time of the slot
    - **event_id**: The ID of the event this slot belongs to
    """
    slot_service = SlotService(db)
    try:
        return slot_service.create_slot(slot_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{slot_id}", response_model=SlotResponse)
def get_slot(
    slot_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific slot by ID
    """
    slot_service = SlotService(db)
    try:
        return slot_service.get_slot(slot_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the slot"
        )

@router.get("/", response_model=List[SlotResponse])
def get_slots(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all slots with optional pagination
    """
    slot_service = SlotService(db)
    try:
        return slot_service.get_slots()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching slots"
        )

@router.put("/{slot_id}", response_model=SlotResponse)
def update_slot(
    slot_id: int,
    slot_data: SlotCreate,
    db: Session = Depends(get_db)
):
    """
    Update a slot's information
    """
    slot_service = SlotService(db)
    try:
        return slot_service.update_slot(slot_id, slot_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the slot"
        )

@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slot(
    slot_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a slot by ID
    """
    slot_service = SlotService(db)
    try:
        slot_service.delete_slot(slot_id)
        return {"message": "Slot deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the slot"
        )