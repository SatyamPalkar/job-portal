"""Application model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base


class Application(Base):
    """Application model for tracking job applications and optimized resumes."""
    
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    
    # Application status
    status = Column(String, default="draft")  # draft, submitted, interviewing, rejected, accepted
    
    # Optimization data
    match_score = Column(Float)  # 0-100 score of resume-job match
    optimizations_applied = Column(Text)  # JSON list of changes made
    suggested_improvements = Column(Text)  # JSON list of additional suggestions
    
    # Cover letter
    cover_letter = Column(Text)
    
    # Notes
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    applied_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")


