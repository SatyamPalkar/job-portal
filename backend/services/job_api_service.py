"""Real job API integration for Jooble and Adzuna."""
import requests
import time
from typing import List, Dict, Optional
from datetime import datetime
from backend.core.config import settings


class JoobleAPI:
    """Jooble API integration for job search."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Jooble API client.
        
        Get your free API key from: https://jooble.org/api/about
        """
        self.api_key = api_key or getattr(settings, 'JOOBLE_API_KEY', '')
        self.base_url = "https://jooble.org/api/"
    
    def search_jobs(
        self,
        keywords: str,
        location: str = "",
        page: int = 1,
        salary: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for jobs using Jooble API.
        
        Args:
            keywords: Job title or keywords
            location: Job location
            page: Page number (1-based)
            salary: Minimum salary
            
        Returns:
            List of job dictionaries
        """
        if not self.api_key:
            print("Warning: Jooble API key not set")
            return []
        
        url = f"{self.base_url}{self.api_key}"
        
        payload = {
            "keywords": keywords,
            "location": location,
            "page": str(page)
        }
        
        if salary:
            payload["salary"] = salary
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                jobs = []
                
                for job in data.get('jobs', []):
                    jobs.append({
                        'title': job.get('title', ''),
                        'company': job.get('company', ''),
                        'location': job.get('location', ''),
                        'description': job.get('snippet', ''),
                        'source': 'Jooble',
                        'source_url': job.get('link', ''),
                        'external_id': f"jooble_{job.get('id', '')}",
                        'salary_range': job.get('salary', ''),
                        'posted_date': self._parse_date(job.get('updated', '')),
                        'job_type': job.get('type', ''),
                    })
                
                return jobs
            else:
                print(f"Jooble API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error calling Jooble API: {e}")
            return []
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime."""
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return datetime.utcnow()


class AdzunaAPI:
    """Adzuna API integration for job search."""
    
    def __init__(self, app_id: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize Adzuna API client.
        
        Get your free API key from: https://developer.adzuna.com/
        """
        self.app_id = app_id or getattr(settings, 'ADZUNA_APP_ID', '')
        self.api_key = api_key or getattr(settings, 'ADZUNA_API_KEY', '')
        self.base_url = "https://api.adzuna.com/v1/api/jobs"
        # Default to US, can be changed to gb, ca, au, etc.
        self.country = getattr(settings, 'ADZUNA_COUNTRY', 'us')
    
    def search_jobs(
        self,
        keywords: str,
        location: str = "",
        page: int = 1,
        results_per_page: int = 20,
        salary_min: Optional[int] = None,
        full_time: Optional[bool] = None
    ) -> List[Dict]:
        """
        Search for jobs using Adzuna API.
        
        Args:
            keywords: Job title or keywords
            location: Job location
            page: Page number (1-based)
            results_per_page: Number of results per page (max 50)
            salary_min: Minimum salary
            full_time: Filter for full-time jobs only
            
        Returns:
            List of job dictionaries
        """
        if not self.app_id or not self.api_key:
            print("Warning: Adzuna API credentials not set")
            return []
        
        url = f"{self.base_url}/{self.country}/search/{page}"
        
        params = {
            'app_id': self.app_id,
            'app_key': self.api_key,
            'what': keywords,
            'results_per_page': results_per_page,
        }
        
        if location:
            params['where'] = location
        
        if salary_min:
            params['salary_min'] = salary_min
        
        if full_time is not None:
            params['full_time'] = 1 if full_time else 0
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                jobs = []
                
                for job in data.get('results', []):
                    # Extract job type
                    job_type = 'Full-time' if job.get('contract_time') == 'full_time' else job.get('contract_time', '')
                    
                    jobs.append({
                        'title': job.get('title', ''),
                        'company': job.get('company', {}).get('display_name', ''),
                        'location': job.get('location', {}).get('display_name', ''),
                        'description': job.get('description', ''),
                        'source': 'Adzuna',
                        'source_url': job.get('redirect_url', ''),
                        'external_id': f"adzuna_{job.get('id', '')}",
                        'salary_range': self._format_salary(job),
                        'posted_date': self._parse_date(job.get('created', '')),
                        'job_type': job_type,
                    })
                
                return jobs
            else:
                print(f"Adzuna API error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Error calling Adzuna API: {e}")
            return []
    
    def _format_salary(self, job: Dict) -> str:
        """Format salary information."""
        salary_min = job.get('salary_min')
        salary_max = job.get('salary_max')
        
        if salary_min and salary_max:
            return f"${salary_min:,.0f} - ${salary_max:,.0f}"
        elif salary_min:
            return f"${salary_min:,.0f}+"
        elif salary_max:
            return f"Up to ${salary_max:,.0f}"
        return ""
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime."""
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return datetime.utcnow()


class UnifiedJobAPI:
    """Unified interface for multiple job APIs."""
    
    def __init__(self):
        """Initialize all job API clients."""
        self.jooble = JoobleAPI()
        self.adzuna = AdzunaAPI()
    
    def search_all_sources(
        self,
        keywords: str,
        location: str = "",
        limit: int = 50,
        salary_min: Optional[int] = None
    ) -> List[Dict]:
        """
        Search jobs from all available sources.
        
        Args:
            keywords: Job title or keywords
            location: Job location
            limit: Maximum total jobs to return
            salary_min: Minimum salary filter
            
        Returns:
            Combined list of jobs from all sources
        """
        all_jobs = []
        
        # Try Jooble
        try:
            jooble_jobs = self.jooble.search_jobs(
                keywords=keywords,
                location=location,
                page=1
            )
            all_jobs.extend(jooble_jobs)
            print(f"Found {len(jooble_jobs)} jobs from Jooble")
        except Exception as e:
            print(f"Jooble search failed: {e}")
        
        # Add delay to respect rate limits
        time.sleep(1)
        
        # Try Adzuna
        try:
            adzuna_jobs = self.adzuna.search_jobs(
                keywords=keywords,
                location=location,
                page=1,
                results_per_page=min(limit, 50),
                salary_min=salary_min
            )
            all_jobs.extend(adzuna_jobs)
            print(f"Found {len(adzuna_jobs)} jobs from Adzuna")
        except Exception as e:
            print(f"Adzuna search failed: {e}")
        
        # Remove duplicates based on title and company
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            key = (job['title'].lower(), job['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs[:limit]

