from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    """Schema for creating an admin comment"""
    fact_check_id: int
    admin_id: int
    comment_text: str

class CommentResponse(BaseModel):
    """Schema for comment response"""
    comment_id: int
    fact_check_id: int
    admin_id: int
    admin_email: str
    comment_text: str
    timestamp: str

class Comment(BaseModel):
    """Complete comment model"""
    comment_id: int
    fact_check_id: int
    admin_id: int
    comment_text: str
    timestamp: datetime
