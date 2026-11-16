from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    role: str
    region_id: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str
    region_id: str = "US-EAST"
