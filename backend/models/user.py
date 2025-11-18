from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr

class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    role: str = Field(..., pattern="^(User|Admin)$", description="Role must be either 'User' or 'Admin'")

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    role: str = Field(..., pattern="^(User|Admin)$", description="Role must be either 'User' or 'Admin'")

class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    user_id: int
    email: str
    role: str
    created_at: str
    last_login: str

class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class User(BaseModel):
    """Complete user model"""
    user_id: int
    email: str
    password_hash: str
    role: str
    created_at: datetime
    last_login: datetime
