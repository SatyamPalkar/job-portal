"""Resume schemas."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ResumeCreate(BaseModel):
    """Schema for creating a resume."""
    title: str
    content: str
    is_original: bool = False


class ResumeResponse(BaseModel):
    """Schema for resume response."""
    id: int
    user_id: int
    title: str
    is_original: bool
    content: str
    raw_text: Optional[str]
    summary: Optional[str]
    keywords: Optional[str]
    action_words: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ResumeOptimizeRequest(BaseModel):
    """Schema for resume optimization request."""
    resume_id: int
    job_id: int
    optimization_level: str = "balanced"  # conservative, balanced, aggressive


class ResumeOptimizeResponse(BaseModel):
    """Schema for resume optimization response."""
    optimized_resume_id: int
    match_score: float
    optimizations_applied: List[str]  # Changed to accept strings
    suggested_improvements: List[str]
    optimized_content: str


