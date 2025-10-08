"""Job search and management routes."""
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.api.dependencies import get_current_active_user
from backend.models.user import User
from backend.models.job import Job
from backend.schemas.job import JobResponse, JobSearch, JobCreate
from backend.services.job_scraper import MockJobScraper
from backend.services.job_api_service import UnifiedJobAPI
from backend.services.nlp_analyzer import NLPAnalyzer
from backend.services.auto_apply_service import rate_limiter
from backend.core.config import settings
from datetime import datetime

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/search", response_model=List[JobResponse])
async def search_jobs(
    search_params: JobSearch,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Search for jobs from real job APIs (Jooble + Adzuna) and save them to database.
    
    This endpoint fetches jobs from multiple sources and stores them in the database.
    Falls back to mock data if API keys are not configured.
    """
    # Try real APIs first
    job_api = UnifiedJobAPI()
    
    # Check if API keys are configured
    has_api_keys = (settings.JOOBLE_API_KEY or settings.ADZUNA_API_KEY)
    
    if has_api_keys:
        # Use real job APIs
        jobs_data = job_api.search_all_sources(
            keywords=search_params.keywords or "",
            location=search_params.location or "",
            limit=search_params.limit
        )
    else:
        # Fallback to mock data
        print("Using mock data - add Jooble/Adzuna API keys for real jobs")
        scraper = MockJobScraper()
        jobs_data = scraper.search_jobs(
            keywords=search_params.keywords or "",
            location=search_params.location or "",
            experience_level=search_params.experience_level,
            job_type=search_params.job_type,
            limit=search_params.limit
        )
    
    # Analyze and save jobs to database
    analyzer = NLPAnalyzer()
    saved_jobs = []
    
    for job_data in jobs_data:
        # Check if job already exists
        existing_job = db.query(Job).filter(
            Job.external_id == job_data.get('external_id')
        ).first()
        
        if existing_job:
            saved_jobs.append(existing_job)
            continue
        
        # Analyze job description
        job_analysis = analyzer.analyze_job_description(job_data['description'])
        
        # Create new job
        db_job = Job(
            title=job_data['title'],
            company=job_data['company'],
            location=job_data.get('location'),
            job_type=job_data.get('job_type'),
            experience_level=job_data.get('experience_level'),
            description=job_data['description'],
            source=job_data.get('source', 'LinkedIn'),
            source_url=job_data.get('source_url'),
            external_id=job_data.get('external_id'),
            keywords=json.dumps(job_analysis.get('all_keywords', [])),
            required_skills=json.dumps(job_analysis.get('required_skills', [])),
            preferred_skills=json.dumps(job_analysis.get('preferred_skills', [])),
            action_words=json.dumps(job_analysis.get('action_words', [])),
            salary_range=job_data.get('salary_range'),
            posted_date=job_data.get('posted_date', datetime.utcnow()),
        )
        
        db.add(db_job)
        saved_jobs.append(db_job)
    
    db.commit()
    
    # Refresh all jobs to get their IDs
    for job in saved_jobs:
        db.refresh(job)
    
    return saved_jobs


@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    keywords: Optional[str] = None,
    location: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all jobs from database with optional filtering."""
    query = db.query(Job).filter(Job.is_active == True)
    
    if keywords:
        query = query.filter(Job.title.contains(keywords) | Job.description.contains(keywords))
    
    if location:
        query = query.filter(Job.location.contains(location))
    
    jobs = query.order_by(Job.posted_date.desc()).offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific job by ID."""
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job


@router.get("/{job_id}/analysis")
async def get_job_analysis(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed analysis of a job posting."""
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Analyze job description
    analyzer = NLPAnalyzer()
    analysis = analyzer.analyze_job_description(job.description)
    
    return {
        'job_id': job.id,
        'title': job.title,
        'company': job.company,
        'analysis': analysis
    }


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a job (admin only - for now just mark as inactive)."""
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    job.is_active = False
    db.commit()
    
    return None


@router.get("/rate-limit/status")
async def get_rate_limit_status(
    current_user: User = Depends(get_current_active_user)
):
    """Get current rate limit status for auto-apply."""
    remaining = rate_limiter.get_remaining()
    
    return {
        'daily_limit': rate_limiter.daily_limit,
        'used_today': rate_limiter.applications_today,
        'remaining_today': remaining,
        'can_apply': rate_limiter.can_apply(),
        'reset_date': str(rate_limiter.last_reset)
    }


