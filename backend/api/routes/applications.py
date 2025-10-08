"""Application tracking routes."""
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.api.dependencies import get_current_active_user
from backend.models.user import User
from backend.models.application import Application
from backend.models.job import Job
from backend.models.resume import Resume
from backend.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate
)
from backend.services.nlp_analyzer import NLPAnalyzer
from backend.services.ai_optimizer import AIResumeOptimizer
from backend.services.professional_resume_generator import ProfessionalResumeGenerator
from backend.services.auto_apply_service import AutoApplyService, rate_limiter
from backend.services.scheduler_service import application_queue
from backend.core.config import settings
from datetime import datetime
import asyncio

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new job application."""
    # Verify job exists
    job = db.query(Job).filter(Job.id == application_data.job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Verify resume exists and belongs to user
    resume = db.query(Resume).filter(
        Resume.id == application_data.resume_id,
        Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Calculate match score
    analyzer = NLPAnalyzer()
    job_analysis = analyzer.analyze_job_description(job.description)
    resume_analysis = analyzer.analyze_resume(resume.content)
    match_score, breakdown = analyzer.calculate_match_score(resume_analysis, job_analysis)
    
    # Generate improvement suggestions
    optimizer = AIResumeOptimizer()
    suggestions = optimizer.suggest_improvements(resume.content, job_analysis, match_score)
    
    # Create application
    db_application = Application(
        user_id=current_user.id,
        job_id=application_data.job_id,
        resume_id=application_data.resume_id,
        match_score=match_score,
        suggested_improvements=json.dumps(suggestions),
        notes=application_data.notes,
    )
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    return db_application


@router.get("/", response_model=List[ApplicationResponse])
async def get_applications(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all applications for current user."""
    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).order_by(Application.created_at.desc()).all()
    
    return applications


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific application."""
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    return application


@router.patch("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    update_data: ApplicationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update application status or details."""
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Update fields
    if update_data.status is not None:
        application.status = update_data.status
        if update_data.status == "submitted":
            application.applied_at = datetime.utcnow()
    
    if update_data.notes is not None:
        application.notes = update_data.notes
    
    if update_data.cover_letter is not None:
        application.cover_letter = update_data.cover_letter
    
    db.commit()
    db.refresh(application)
    
    return application


@router.post("/{application_id}/generate-cover-letter")
async def generate_cover_letter(
    application_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate a cover letter for an application."""
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Get job and resume
    job = db.query(Job).filter(Job.id == application.job_id).first()
    resume = db.query(Resume).filter(Resume.id == application.resume_id).first()
    
    # Generate cover letter
    optimizer = AIResumeOptimizer()
    cover_letter = optimizer.generate_cover_letter(
        resume.content,
        job.description,
        job.company,
        job.title
    )
    
    # Save cover letter
    application.cover_letter = cover_letter
    db.commit()
    
    return {
        'application_id': application_id,
        'cover_letter': cover_letter
    }


@router.get("/{application_id}/download/{format}")
async def download_application_resume(
    application_id: int,
    format: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Download application resume in specified format (pdf, docx, txt)."""
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Get resume
    resume = db.query(Resume).filter(Resume.id == application.resume_id).first()
    job = db.query(Job).filter(Job.id == application.job_id).first()
    
    # Prepare resume data
    resume_data = {
        'name': current_user.full_name or current_user.username,
        'email': json.loads(resume.keywords)[0] if resume.keywords else current_user.email,
        'summary': resume.summary,
        'experience': resume.experience,
        'education': resume.education,
        'skills': resume.skills,
        'projects': resume.projects,
        'certifications': resume.certifications,
    }
    
    # Generate resume with professional formatting
    generator = ProfessionalResumeGenerator()
    
    try:
        if format == 'pdf':
            file_path = generator.generate_pdf(resume_data, f"resume_{application_id}.pdf")
        elif format == 'docx':
            file_path = generator.generate_docx(resume_data, f"resume_{application_id}.docx")
        elif format == 'txt':
            file_path = generator.generate_txt(resume_data, f"resume_{application_id}.txt")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid format. Use: pdf, docx, or txt"
            )
        
        return {
            'file_path': file_path,
            'format': format,
            'message': f'Resume generated successfully for job: {job.title}'
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating resume: {str(e)}"
        )


@router.post("/{application_id}/auto-apply")
async def auto_apply_to_job(
    application_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Automatically apply to job using Playwright automation.
    
    This will:
    1. Check rate limits (50 applications/day)
    2. Queue the application for processing
    3. Auto-fill the application form
    4. Attach optimized resume
    5. Return status (does not auto-submit for safety)
    """
    if not settings.AUTO_APPLY_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Auto-apply feature is disabled. Set AUTO_APPLY_ENABLED=true in .env"
        )
    
    # Check rate limit
    if not rate_limiter.can_apply():
        remaining = rate_limiter.get_remaining()
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Daily application limit reached ({rate_limiter.daily_limit}). {remaining} applications remaining for today."
        )
    
    # Get application
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Get job and resume
    job = db.query(Job).filter(Job.id == application.job_id).first()
    resume = db.query(Resume).filter(Resume.id == application.resume_id).first()
    
    if not job or not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job or resume not found"
        )
    
    # Generate resume file if needed
    generator = ProfessionalResumeGenerator()
    resume_data = {
        'name': current_user.full_name or current_user.username,
        'email': current_user.email,
        'summary': resume.summary,
        'experience': resume.experience,
        'education': resume.education,
        'skills': resume.skills,
        'projects': resume.projects,
    }
    
    resume_file = generator.generate_pdf(resume_data, f"resume_app_{application_id}.pdf")
    
    # Add to application queue
    await application_queue.add_application(
        job_url=job.source_url or "",
        resume_path=resume_file,
        cover_letter=application.cover_letter,
        user_id=current_user.id
    )
    
    return {
        'status': 'queued',
        'message': 'Application queued for processing',
        'application_id': application_id,
        'queue_position': len(application_queue.queue),
        'estimated_processing_time': f"{len(application_queue.queue) * 60} seconds",
        'daily_limit_remaining': rate_limiter.get_remaining() - 1
    }


@router.get("/queue/status")
async def get_queue_status(
    current_user: User = Depends(get_current_active_user)
):
    """Get status of the auto-apply queue."""
    return {
        'queue_length': len(application_queue.queue),
        'processing': application_queue.processing,
        'daily_limit': rate_limiter.daily_limit,
        'remaining_today': rate_limiter.get_remaining(),
        'next_reset': str(datetime.now().date())
    }


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an application."""
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    db.delete(application)
    db.commit()
    
    return None


