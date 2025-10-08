"""Application schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApplicationCreate(BaseModel):
    """Schema for creating an application."""
    job_id: int
    resume_id: int
    notes: Optional[str] = None


class ApplicationResponse(BaseModel):
    """Schema for application response."""
    id: int
    user_id: int
    job_id: int
    resume_id: int
    status: str
    match_score: Optional[float]
    optimizations_applied: Optional[str]
    suggested_improvements: Optional[str]
    cover_letter: Optional[str]
    notes: Optional[str]
    created_at: datetime
    applied_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ApplicationUpdate(BaseModel):
    """Schema for updating an application."""
    status: Optional[str] = None
    notes: Optional[str] = None
    cover_letter: Optional[str] = None


