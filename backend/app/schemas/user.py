from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    ai_disclosure_accepted: bool
    data_use_accepted: bool
    display_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID4
    email: str
    display_name: Optional[str]
    ai_disclosure_accepted: bool
    data_use_accepted: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
