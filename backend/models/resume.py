"""Resume model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base


class Resume(Base):
    """Resume model for storing user resumes."""
    
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Resume metadata
    title = Column(String, nullable=False)
    is_original = Column(Boolean, default=False)  # True if this is the user's base resume
    
    # Resume content
    content = Column(Text, nullable=False)  # Structured JSON content
    raw_text = Column(Text)  # Plain text version
    file_path = Column(String)  # Path to uploaded file
    
    # Parsed sections
    summary = Column(Text)
    experience = Column(Text)  # JSON
    education = Column(Text)  # JSON
    skills = Column(Text)  # JSON
    projects = Column(Text)  # JSON
    certifications = Column(Text)  # JSON
    
    # Analysis
    keywords = Column(Text)  # JSON list of extracted keywords
    action_words = Column(Text)  # JSON list of action words used
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")


