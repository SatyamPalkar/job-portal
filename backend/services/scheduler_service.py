"""Job scheduler service for automated job fetching."""
import asyncio
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal
from backend.services.job_api_service import UnifiedJobAPI
from backend.services.nlp_analyzer import NLPAnalyzer
from backend.models.job import Job
from backend.models.user import User
import json


class JobScheduler:
    """Automated job fetching and processing scheduler."""
    
    def __init__(self):
        """Initialize the scheduler."""
        self.scheduler = AsyncIOScheduler()
        self.job_api = UnifiedJobAPI()
        self.analyzer = NLPAnalyzer()
    
    def start(self):
        """Start the scheduler."""
        # Fetch jobs every 6 hours
        self.scheduler.add_job(
            self.fetch_jobs_for_all_users,
            CronTrigger(hour='*/6'),  # Every 6 hours
            id='fetch_jobs',
            name='Fetch new jobs',
            replace_existing=True
        )
        
        # Daily cleanup of old jobs (30 days)
        self.scheduler.add_job(
            self.cleanup_old_jobs,
            CronTrigger(hour=2, minute=0),  # 2 AM daily
            id='cleanup_jobs',
            name='Cleanup old jobs',
            replace_existing=True
        )
        
        self.scheduler.start()
        print("✓ Job scheduler started")
    
    def stop(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        print("✓ Job scheduler stopped")
    
    async def fetch_jobs_for_all_users(self):
        """Fetch jobs for all active users based on their preferences."""
        db = SessionLocal()
        
        try:
            # Get all active users with target roles
            users = db.query(User).filter(
                User.is_active == True,
                User.target_roles.isnot(None)
            ).all()
            
            print(f"Fetching jobs for {len(users)} users...")
            
            for user in users:
                await self._fetch_jobs_for_user(user, db)
                # Add delay between users
                await asyncio.sleep(5)
            
        except Exception as e:
            print(f"Error in scheduled job fetch: {e}")
        finally:
            db.close()
    
    async def _fetch_jobs_for_user(self, user: User, db: Session):
        """Fetch jobs for a specific user."""
        try:
            # Parse user preferences
            target_roles = json.loads(user.target_roles) if user.target_roles else []
            
            if not target_roles:
                return
            
            # Fetch jobs for each target role
            for role in target_roles[:3]:  # Limit to 3 roles per user
                jobs_data = self.job_api.search_all_sources(
                    keywords=role,
                    location="",  # Can be customized per user
                    limit=20
                )
                
                # Save jobs to database
                for job_data in jobs_data:
                    # Check if job already exists
                    existing = db.query(Job).filter(
                        Job.external_id == job_data.get('external_id')
                    ).first()
                    
                    if existing:
                        continue
                    
                    # Analyze job description
                    job_analysis = self.analyzer.analyze_job_description(
                        job_data.get('description', '')
                    )
                    
                    # Create new job
                    new_job = Job(
                        title=job_data['title'],
                        company=job_data['company'],
                        location=job_data.get('location'),
                        job_type=job_data.get('job_type'),
                        description=job_data['description'],
                        source=job_data.get('source', 'API'),
                        source_url=job_data.get('source_url'),
                        external_id=job_data.get('external_id'),
                        keywords=json.dumps(job_analysis.get('all_keywords', [])),
                        required_skills=json.dumps(job_analysis.get('required_skills', [])),
                        preferred_skills=json.dumps(job_analysis.get('preferred_skills', [])),
                        action_words=json.dumps(job_analysis.get('action_words', [])),
                        salary_range=job_data.get('salary_range'),
                        posted_date=job_data.get('posted_date', datetime.utcnow()),
                    )
                    
                    db.add(new_job)
                
                db.commit()
                print(f"  Added {len(jobs_data)} jobs for role: {role}")
                
                # Delay between searches
                await asyncio.sleep(2)
                
        except Exception as e:
            print(f"Error fetching jobs for user {user.username}: {e}")
    
    async def cleanup_old_jobs(self):
        """Remove job postings older than 30 days."""
        db = SessionLocal()
        
        try:
            from datetime import timedelta
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            # Mark old jobs as inactive instead of deleting
            old_jobs = db.query(Job).filter(
                Job.posted_date < thirty_days_ago,
                Job.is_active == True
            ).all()
            
            for job in old_jobs:
                job.is_active = False
            
            db.commit()
            print(f"Cleaned up {len(old_jobs)} old jobs")
            
        except Exception as e:
            print(f"Error in cleanup: {e}")
        finally:
            db.close()


class ApplicationQueue:
    """Queue for managing automated job applications."""
    
    def __init__(self):
        """Initialize application queue."""
        self.queue = []
        self.processing = False
    
    async def add_application(
        self,
        job_url: str,
        resume_path: str,
        cover_letter: Optional[str] = None,
        user_id: int = None
    ):
        """Add an application to the queue."""
        self.queue.append({
            'job_url': job_url,
            'resume_path': resume_path,
            'cover_letter': cover_letter,
            'user_id': user_id,
            'queued_at': datetime.utcnow()
        })
    
    async def process_queue(self):
        """Process applications in the queue with rate limiting."""
        if self.processing:
            print("Queue is already being processed")
            return
        
        self.processing = True
        auto_apply = AutoApplyService()
        
        try:
            from backend.services.auto_apply_service import rate_limiter
            
            while self.queue and rate_limiter.can_apply():
                application_data = self.queue.pop(0)
                
                # Check rate limit
                remaining = rate_limiter.get_remaining()
                if remaining <= 0:
                    print(f"Daily limit reached. {len(self.queue)} applications remain in queue.")
                    break
                
                # Process application
                print(f"Processing application {application_data['job_url']} ({remaining} remaining today)")
                
                result = await auto_apply.apply_to_linkedin_job(
                    job_url=application_data['job_url'],
                    resume_path=application_data['resume_path'],
                    cover_letter_text=application_data.get('cover_letter')
                )
                
                if result['success']:
                    rate_limiter.record_application()
                    print(f"  ✓ Application prepared successfully")
                else:
                    print(f"  ✗ Application failed: {result['message']}")
                
                # Random delay between applications
                delay = auto_apply.get_random_delay()
                print(f"  Waiting {delay} seconds before next application...")
                await asyncio.sleep(delay)
            
            if self.queue:
                print(f"{len(self.queue)} applications remain in queue for tomorrow")
                
        except Exception as e:
            print(f"Error processing queue: {e}")
        finally:
            self.processing = False


# Global instances
job_scheduler = JobScheduler()
application_queue = ApplicationQueue()

