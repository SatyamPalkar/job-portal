"""Resume management routes."""
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.api.dependencies import get_current_active_user
from backend.models.user import User
from backend.models.resume import Resume
from backend.schemas.resume import (
    ResumeCreate,
    ResumeResponse,
    ResumeOptimizeRequest,
    ResumeOptimizeResponse
)
from backend.models.job import Job
from backend.models.application import Application
from backend.services.resume_parser import ResumeParser
from backend.services.nlp_analyzer import NLPAnalyzer
from backend.services.ai_optimizer import AIResumeOptimizer
from backend.services.resume_generator import ResumeGenerator
from pathlib import Path
import shutil

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    resume_data: ResumeCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new resume."""
    # Parse resume content
    parser = ResumeParser()
    parsed_data = parser.parse_text_content(resume_data.content)
    
    # Create resume in database
    db_resume = Resume(
        user_id=current_user.id,
        title=resume_data.title,
        is_original=resume_data.is_original,
        content=resume_data.content,
        raw_text=parsed_data.get('raw_text', ''),
        summary=parsed_data.get('summary', ''),
        experience=json.dumps(parsed_data.get('experience', [])),
        education=json.dumps(parsed_data.get('education', [])),
        skills=json.dumps(parsed_data.get('skills', [])),
        projects=json.dumps(parsed_data.get('projects', [])),
        certifications=json.dumps(parsed_data.get('certifications', [])),
        keywords=json.dumps(parsed_data.get('keywords', [])),
        action_words=json.dumps(parsed_data.get('action_words', [])),
    )
    
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    return db_resume


@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    title: str = "My Resume",
    is_original: bool = True,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload a resume file (PDF, DOCX, TXT)."""
    # Validate file extension
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file
    upload_dir = Path("./uploads/resumes")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_dir / f"{current_user.id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Parse resume
    parser = ResumeParser()
    try:
        parsed_data = parser.parse_file(str(file_path))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error parsing resume: {str(e)}"
        )
    
    # Create resume in database
    db_resume = Resume(
        user_id=current_user.id,
        title=title,
        is_original=is_original,
        content=parsed_data.get('raw_text', ''),
        raw_text=parsed_data.get('raw_text', ''),
        file_path=str(file_path),
        summary=parsed_data.get('summary', ''),
        experience=json.dumps(parsed_data.get('experience', [])),
        education=json.dumps(parsed_data.get('education', [])),
        skills=json.dumps(parsed_data.get('skills', [])),
        projects=json.dumps(parsed_data.get('projects', [])),
        certifications=json.dumps(parsed_data.get('certifications', [])),
        keywords=json.dumps(parsed_data.get('keywords', [])),
        action_words=json.dumps(parsed_data.get('action_words', [])),
    )
    
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    return db_resume


@router.get("/", response_model=List[ResumeResponse])
async def get_resumes(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all resumes for current user."""
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return resumes


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific resume."""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    return resume


@router.post("/optimize", response_model=ResumeOptimizeResponse)
async def optimize_resume(
    request: ResumeOptimizeRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Optimize resume for a specific job."""
    # Get resume
    resume = db.query(Resume).filter(
        Resume.id == request.resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Get job
    job = db.query(Job).filter(Job.id == request.job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Analyze job and resume
    analyzer = NLPAnalyzer()
    job_analysis = analyzer.analyze_job_description(job.description)
    resume_analysis = analyzer.analyze_resume(resume.content)
    
    # Calculate match score
    match_score, breakdown = analyzer.calculate_match_score(resume_analysis, job_analysis)
    
    # Optimize resume using AI
    optimizer = AIResumeOptimizer()
    optimization_result = optimizer.optimize_resume(
        resume.content,
        job.description,
        job_analysis,
        resume_analysis,
        request.optimization_level
    )
    
    # Create new optimized resume
    optimized_resume = Resume(
        user_id=current_user.id,
        title=f"{resume.title} - Optimized for {job.title}",
        is_original=False,
        content=optimization_result['optimized_content'],
        raw_text=optimization_result['optimized_content'],
        summary=resume.summary,
        experience=resume.experience,
        education=resume.education,
        skills=resume.skills,
        projects=resume.projects,
        certifications=resume.certifications,
        keywords=json.dumps(job_analysis.get('all_keywords', [])),
        action_words=json.dumps(optimization_result.get('action_words_added', [])),
    )
    
    db.add(optimized_resume)
    db.commit()
    db.refresh(optimized_resume)
    
    # Create application record
    application = Application(
        user_id=current_user.id,
        job_id=job.id,
        resume_id=optimized_resume.id,
        match_score=match_score,
        optimizations_applied=json.dumps(optimization_result.get('optimizations_applied', [])),
        suggested_improvements=json.dumps(optimization_result.get('suggested_improvements', [])),
    )
    
    db.add(application)
    db.commit()
    
    return ResumeOptimizeResponse(
        optimized_resume_id=optimized_resume.id,
        match_score=match_score,
        optimizations_applied=optimization_result.get('optimizations_applied', []),
        suggested_improvements=optimization_result.get('suggested_improvements', []),
        optimized_content=optimization_result['optimized_content']
    )


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a resume."""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    db.delete(resume)
    db.commit()
    
    return None


