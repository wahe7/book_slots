from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class AdminBase(BaseModel):
    email: EmailStr = Field(..., example="admin@example.com")
    name: str = Field(..., example="Admin User")

class AdminCreate(AdminBase):
    password: str = Field(..., min_length=6, example="securepassword123")

class AdminResponse(AdminBase):
    id: int

    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    email: EmailStr = Field(..., example="admin@example.com")
    password: str = Field(..., example="securepassword123")

class LoginResponse(BaseModel):
    success: bool
    message: str
    admin: Optional[AdminResponse] = None
