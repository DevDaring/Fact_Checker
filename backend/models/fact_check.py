from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class FactCheckCreate(BaseModel):
    """Schema for creating a fact check"""
    user_id: int
    upload_type: str = Field(..., pattern="^(video|audio|image)$")
    file_path: str

class FactCheckProcess(BaseModel):
    """Schema for processing a fact check"""
    file_id: str
    upload_type: str = Field(..., pattern="^(video|audio|image)$")

class Citation(BaseModel):
    """Schema for citation"""
    title: str
    url: str
    snippet: Optional[str] = None

class FactCheckResult(BaseModel):
    """Schema for fact check result"""
    fact_check_id: int
    extracted_text: Optional[str] = None
    gemini_response: str
    citations: List[dict]
    timestamp: str

class FactCheckResponse(BaseModel):
    """Schema for fact check response"""
    fact_check_id: int
    user_id: int
    upload_type: str
    file_path: str
    extracted_text: Optional[str]
    gemini_response: str
    citations: List[dict]
    timestamp: str
    admin_comments: Optional[List[dict]] = []

class FactCheckHistory(BaseModel):
    """Schema for fact check history"""
    fact_check_id: int
    upload_type: str
    timestamp: str
    gemini_response: str
    has_comments: bool = False

class FactCheck(BaseModel):
    """Complete fact check model"""
    fact_check_id: int
    user_id: int
    upload_type: str
    file_path: str
    extracted_text: Optional[str]
    gemini_response: str
    citations: str  # JSON string in CSV
    timestamp: datetime
