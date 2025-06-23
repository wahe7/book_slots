from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from src.db.database import get_db
from src.schemas.admin import AdminLogin, LoginResponse
from src.db.models import Admin

router = APIRouter(prefix="/admin", tags=["admin"])



@router.post("/login", response_model=LoginResponse)
async def login_admin(login_data: AdminLogin, db: Session = Depends(get_db)):
    """
    Authenticate an admin user with email and password
    """
    admin = db.query(Admin).filter(Admin.email == login_data.email).first()
    print(admin)
    if not admin or login_data.password != admin.password:
        return {
            "success": False,
            "message": "Incorrect email or password",
            "admin": None
        }
    
    return {
        "success": True,
        "message": "Login successful",
        "admin": {
            "id": admin.id,
            "name": admin.name,
            "email": admin.email,
        }
    }
