"""
Pydantic schemas for User, Auth, and Token representation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.user import UserRole


class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    role: UserRole = UserRole.STUDENT
    department: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole
    username: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None
