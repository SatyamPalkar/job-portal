"""Job schemas."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class JobSearch(BaseModel):
    """Schema for job search request."""
    keywords: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    limit: int = 20


class JobResponse(BaseModel):
    """Schema for job response."""
    id: int
    title: str
    company: str
    location: Optional[str]
    job_type: Optional[str]
    experience_level: Optional[str]
    description: str
    requirements: Optional[str]
    responsibilities: Optional[str]
    source: str
    source_url: Optional[str]
    keywords: Optional[str]
    required_skills: Optional[str]
    preferred_skills: Optional[str]
    salary_range: Optional[str]
    posted_date: Optional[datetime]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class JobCreate(BaseModel):
    """Schema for creating a job (internal use)."""
    title: str
    company: str
    description: str
    location: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    source: str = "LinkedIn"
    source_url: Optional[str] = None
    external_id: Optional[str] = None


