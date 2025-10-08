"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.core.config import settings
from backend.core.database import init_db, engine
from backend.models import User, Resume, Job, Application
from backend.api.routes import auth, resumes, jobs, applications


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    print("🚀 Starting Resume Optimizer SaaS...")
    
    # Create database tables
    init_db()
    print("✓ Database initialized")
    
    # Start job scheduler (optional)
    if hasattr(settings, 'ENABLE_JOB_SCHEDULER') and settings.ENABLE_JOB_SCHEDULER:
        from backend.services.scheduler_service import job_scheduler
        job_scheduler.start()
        print("✓ Job scheduler started")
    
    yield
    
    # Shutdown
    if hasattr(settings, 'ENABLE_JOB_SCHEDULER') and settings.ENABLE_JOB_SCHEDULER:
        from backend.services.scheduler_service import job_scheduler
        job_scheduler.stop()
        print("✓ Job scheduler stopped")

# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered resume optimization SaaS platform with automated job applications",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(resumes.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(applications.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )


