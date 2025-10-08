"""Auto-apply service using Playwright for job application automation."""
import asyncio
import time
from typing import Dict, Optional, List
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser
from datetime import datetime


class AutoApplyService:
    """Automate job applications using Playwright."""
    
    def __init__(self, headless: bool = True):
        """
        Initialize the auto-apply service.
        
        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.apply_delay = (20, 90)  # Delay range in seconds
        self.daily_limit = 50
    
    async def apply_to_linkedin_job(
        self,
        job_url: str,
        resume_path: str,
        cover_letter_text: Optional[str] = None,
        user_credentials: Optional[Dict] = None
    ) -> Dict:
        """
        Auto-apply to a LinkedIn job posting.
        
        Args:
            job_url: URL of the job posting
            resume_path: Path to resume file
            cover_letter_text: Optional cover letter
            user_credentials: LinkedIn credentials {'email': '', 'password': ''}
            
        Returns:
            Dict with application status
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Navigate to job
                await page.goto(job_url)
                await page.wait_for_load_state('networkidle')
                
                # Check if login is required
                if user_credentials and await self._is_login_required(page):
                    await self._login_linkedin(page, user_credentials)
                
                # Find and click Easy Apply button
                easy_apply_button = await page.query_selector('button:has-text("Easy Apply"), button:has-text("Apply")')
                
                if not easy_apply_button:
                    return {
                        'success': False,
                        'message': 'Easy Apply not available for this job',
                        'job_url': job_url
                    }
                
                await easy_apply_button.click()
                await page.wait_for_timeout(2000)
                
                # Fill application form
                await self._fill_application_form(page, resume_path, cover_letter_text)
                
                # Submit application
                submit_button = await page.query_selector('button:has-text("Submit application"), button:has-text("Submit")')
                
                if submit_button:
                    # Note: In production, you might want manual confirmation
                    # await submit_button.click()
                    
                    # For safety, we'll just prepare but not submit
                    return {
                        'success': True,
                        'message': 'Application form filled and ready to submit',
                        'job_url': job_url,
                        'auto_submitted': False,
                        'note': 'Manual review recommended before submission'
                    }
                else:
                    return {
                        'success': False,
                        'message': 'Could not find submit button',
                        'job_url': job_url
                    }
                
            except Exception as e:
                return {
                    'success': False,
                    'message': f'Error during application: {str(e)}',
                    'job_url': job_url
                }
            
            finally:
                await browser.close()
    
    async def _is_login_required(self, page: Page) -> bool:
        """Check if login is required."""
        login_button = await page.query_selector('a:has-text("Sign in")')
        return login_button is not None
    
    async def _login_linkedin(self, page: Page, credentials: Dict):
        """Login to LinkedIn."""
        try:
            # Click sign in
            await page.click('a:has-text("Sign in")')
            await page.wait_for_timeout(2000)
            
            # Fill credentials
            await page.fill('input[name="session_key"]', credentials['email'])
            await page.fill('input[name="session_password"]', credentials['password'])
            
            # Submit
            await page.click('button[type="submit"]')
            await page.wait_for_load_state('networkidle')
            
        except Exception as e:
            print(f"Login error: {e}")
    
    async def _fill_application_form(
        self,
        page: Page,
        resume_path: str,
        cover_letter: Optional[str] = None
    ):
        """Fill out the application form."""
        try:
            # Upload resume
            resume_upload = await page.query_selector('input[type="file"]')
            if resume_upload:
                await resume_upload.set_input_files(resume_path)
                await page.wait_for_timeout(2000)
            
            # Fill cover letter if available
            if cover_letter:
                cover_letter_input = await page.query_selector('textarea[name*="cover"], textarea[placeholder*="cover"]')
                if cover_letter_input:
                    await cover_letter_input.fill(cover_letter)
            
            # Fill any text inputs with placeholder data
            text_inputs = await page.query_selector_all('input[type="text"]:visible')
            for input_elem in text_inputs:
                placeholder = await input_elem.get_attribute('placeholder')
                if placeholder and not await input_elem.input_value():
                    # Fill with reasonable defaults based on placeholder
                    if 'phone' in placeholder.lower():
                        await input_elem.fill('555-555-5555')
                    elif 'city' in placeholder.lower() or 'location' in placeholder.lower():
                        await input_elem.fill('San Francisco')
            
            await page.wait_for_timeout(1000)
            
        except Exception as e:
            print(f"Form fill error: {e}")
    
    def get_random_delay(self) -> int:
        """Get a random delay between min and max range."""
        import random
        return random.randint(self.apply_delay[0], self.apply_delay[1])


class RateLimiter:
    """Rate limiter for job applications."""
    
    def __init__(self, daily_limit: int = 50, storage_path: str = "./data/rate_limits.json"):
        """
        Initialize rate limiter.
        
        Args:
            daily_limit: Maximum applications per day
            storage_path: Path to store rate limit data
        """
        self.daily_limit = daily_limit
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.applications_today = self._load_count()
        self.last_reset = datetime.now().date()
    
    def can_apply(self) -> bool:
        """Check if we can apply to more jobs today."""
        self._check_reset()
        return self.applications_today < self.daily_limit
    
    def record_application(self):
        """Record a new application."""
        self._check_reset()
        self.applications_today += 1
        self._save_count()
    
    def get_remaining(self) -> int:
        """Get remaining applications for today."""
        self._check_reset()
        return max(0, self.daily_limit - self.applications_today)
    
    def _check_reset(self):
        """Check if we need to reset the daily counter."""
        today = datetime.now().date()
        if today > self.last_reset:
            self.applications_today = 0
            self.last_reset = today
            self._save_count()
    
    def _load_count(self) -> int:
        """Load application count from storage."""
        try:
            if self.storage_path.exists():
                import json
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    if data.get('date') == str(datetime.now().date()):
                        return data.get('count', 0)
        except Exception as e:
            print(f"Error loading rate limit data: {e}")
        return 0
    
    def _save_count(self):
        """Save application count to storage."""
        try:
            import json
            with open(self.storage_path, 'w') as f:
                json.dump({
                    'date': str(datetime.now().date()),
                    'count': self.applications_today
                }, f)
        except Exception as e:
            print(f"Error saving rate limit data: {e}")


# Initialize global rate limiter
rate_limiter = RateLimiter(daily_limit=50)

