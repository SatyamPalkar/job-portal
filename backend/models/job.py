"""Job model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base


class Job(Base):
    """Job model for storing scraped job postings."""
    
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Job details
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    location = Column(String)
    job_type = Column(String)  # Full-time, Part-time, Contract, etc.
    experience_level = Column(String)  # Entry, Mid, Senior, etc.
    
    # Job description
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    responsibilities = Column(Text)
    
    # Source information
    source = Column(String, default="LinkedIn")  # LinkedIn, Indeed, etc.
    source_url = Column(String)
    external_id = Column(String, unique=True, index=True)  # Job ID from source
    
    # Parsed data
    keywords = Column(Text)  # JSON list of extracted keywords
    required_skills = Column(Text)  # JSON list
    preferred_skills = Column(Text)  # JSON list
    action_words = Column(Text)  # JSON list of action words in JD
    
    # Metadata
    salary_range = Column(String)
    posted_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = relationship("Application", back_populates="job")


