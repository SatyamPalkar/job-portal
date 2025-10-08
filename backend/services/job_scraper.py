"""LinkedIn job scraper service."""
import re
import time
from typing import List, Dict, Optional
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# Selenium is optional - only needed for real scraping
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class LinkedInJobScraper:
    """
    Scraper for LinkedIn job postings.
    
    Note: LinkedIn has anti-scraping measures. For production use:
    1. Use LinkedIn's official API (requires partnership)
    2. Implement proper rate limiting
    3. Use rotating proxies
    4. Consider using paid scraping services like ScraperAPI
    """
    
    def __init__(self, headless: bool = True):
        """Initialize the scraper."""
        self.headless = headless
        self.base_url = "https://www.linkedin.com"
        
    def _get_driver(self):
        """Create and configure Chrome WebDriver."""
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium not installed. Use MockJobScraper instead or install selenium.")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    def search_jobs(
        self,
        keywords: str,
        location: str = "",
        experience_level: Optional[str] = None,
        job_type: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        Search for jobs on LinkedIn.
        
        Args:
            keywords: Job title or keywords to search for
            location: Job location
            experience_level: Entry level, Associate, Mid-Senior level, Director, Executive
            job_type: Full-time, Part-time, Contract, Temporary, Volunteer, Internship
            limit: Maximum number of jobs to return
            
        Returns:
            List of job dictionaries
        """
        jobs = []
        
        # Build search URL
        search_url = f"{self.base_url}/jobs/search/?"
        params = []
        
        if keywords:
            params.append(f"keywords={keywords.replace(' ', '%20')}")
        if location:
            params.append(f"location={location.replace(' ', '%20')}")
        
        search_url += "&".join(params)
        
        try:
            driver = self._get_driver()
            driver.get(search_url)
            
            # Wait for job listings to load
            time.sleep(3)
            
            # Scroll to load more jobs
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Parse job cards
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_cards = soup.find_all('div', class_='base-card')
            
            for card in job_cards[:limit]:
                try:
                    job_data = self._parse_job_card(card, driver)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    print(f"Error parsing job card: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            print(f"Error scraping jobs: {e}")
        
        return jobs
    
    def _parse_job_card(self, card, driver) -> Optional[Dict]:
        """Parse a job card to extract job details."""
        try:
            # Extract basic info from card
            title_elem = card.find('h3', class_='base-search-card__title')
            company_elem = card.find('h4', class_='base-search-card__subtitle')
            location_elem = card.find('span', class_='job-search-card__location')
            link_elem = card.find('a', class_='base-card__full-link')
            
            if not title_elem or not company_elem or not link_elem:
                return None
            
            title = title_elem.text.strip()
            company = company_elem.text.strip()
            location = location_elem.text.strip() if location_elem else ""
            job_url = link_elem.get('href', '')
            
            # Extract job ID from URL
            job_id_match = re.search(r'/jobs/view/(\d+)', job_url)
            external_id = job_id_match.group(1) if job_id_match else None
            
            # Get full job description (would need to click and load)
            # For demo, using placeholder
            description = "Job description would be loaded here by clicking the job card"
            
            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'source': 'LinkedIn',
                'source_url': job_url,
                'external_id': external_id,
                'posted_date': datetime.utcnow(),
            }
            
            return job_data
            
        except Exception as e:
            print(f"Error in _parse_job_card: {e}")
            return None
    
    def get_job_details(self, job_url: str) -> Optional[Dict]:
        """
        Get detailed information for a specific job posting.
        
        Args:
            job_url: URL of the job posting
            
        Returns:
            Dictionary with detailed job information
        """
        try:
            driver = self._get_driver()
            driver.get(job_url)
            
            # Wait for job description to load
            time.sleep(3)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract job details
            title = soup.find('h1', class_='topcard__title')
            company = soup.find('a', class_='topcard__org-name-link')
            location = soup.find('span', class_='topcard__flavor--bullet')
            description_elem = soup.find('div', class_='show-more-less-html__markup')
            
            job_data = {
                'title': title.text.strip() if title else '',
                'company': company.text.strip() if company else '',
                'location': location.text.strip() if location else '',
                'description': description_elem.text.strip() if description_elem else '',
                'source_url': job_url,
            }
            
            driver.quit()
            return job_data
            
        except Exception as e:
            print(f"Error getting job details: {e}")
            return None


class MockJobScraper:
    """
    Mock job scraper for development/testing without actual web scraping.
    Returns sample job data.
    """
    
    def search_jobs(
        self,
        keywords: str,
        location: str = "",
        experience_level: Optional[str] = None,
        job_type: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """Return mock job data."""
        
        mock_jobs = [
            {
                'title': 'Senior Software Engineer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'job_type': 'Full-time',
                'experience_level': 'Mid-Senior level',
                'description': """
We are seeking a talented Senior Software Engineer to join our growing team. 

Responsibilities:
- Design and develop scalable web applications
- Collaborate with cross-functional teams
- Mentor junior developers
- Participate in code reviews
- Implement best practices and coding standards

Requirements:
- 5+ years of experience in software development
- Strong proficiency in Python, JavaScript, or Java
- Experience with React, Node.js, or similar frameworks
- Solid understanding of database design and optimization
- Experience with cloud platforms (AWS, GCP, or Azure)
- Excellent problem-solving skills
- Strong communication and teamwork abilities

Preferred:
- Experience with microservices architecture
- Knowledge of DevOps practices and CI/CD pipelines
- Contributions to open-source projects
                """,
                'source': 'LinkedIn',
                'source_url': 'https://linkedin.com/jobs/view/123456',
                'external_id': '123456',
                'posted_date': datetime.utcnow(),
                'salary_range': '$120,000 - $180,000'
            },
            {
                'title': 'Full Stack Developer',
                'company': 'StartUp Inc',
                'location': 'Remote',
                'job_type': 'Full-time',
                'experience_level': 'Mid-Senior level',
                'description': """
Join our innovative startup as a Full Stack Developer!

What You'll Do:
- Build and maintain our web application platform
- Develop RESTful APIs and microservices
- Create responsive user interfaces
- Optimize application performance
- Work with modern technologies and frameworks

What We're Looking For:
- 3+ years of full-stack development experience
- Proficiency in React and Node.js
- Experience with TypeScript
- Strong understanding of database technologies (PostgreSQL, MongoDB)
- Familiarity with Docker and Kubernetes
- Passion for clean, maintainable code

Bonus Points:
- Experience with GraphQL
- Knowledge of AWS or similar cloud platforms
- Experience in agile development environments
                """,
                'source': 'LinkedIn',
                'source_url': 'https://linkedin.com/jobs/view/123457',
                'external_id': '123457',
                'posted_date': datetime.utcnow(),
                'salary_range': '$100,000 - $150,000'
            },
            {
                'title': 'Python Backend Engineer',
                'company': 'Data Solutions LLC',
                'location': 'New York, NY',
                'job_type': 'Full-time',
                'experience_level': 'Mid-Senior level',
                'description': """
We're hiring a Python Backend Engineer to work on our data platform!

Key Responsibilities:
- Design and implement scalable backend services
- Develop data processing pipelines
- Integrate with third-party APIs
- Optimize database queries and performance
- Write clean, testable code

Required Skills:
- 4+ years of Python development experience
- Strong knowledge of Django or Flask
- Experience with PostgreSQL and Redis
- Understanding of RESTful API design
- Familiarity with message queues (RabbitMQ, Kafka)
- Experience with unit testing and TDD

Nice to Have:
- Experience with data engineering tools
- Knowledge of machine learning frameworks
- Contributions to Python community
                """,
                'source': 'LinkedIn',
                'source_url': 'https://linkedin.com/jobs/view/123458',
                'external_id': '123458',
                'posted_date': datetime.utcnow(),
                'salary_range': '$110,000 - $160,000'
            }
        ]
        
        # Filter by keywords (simple simulation)
        filtered_jobs = []
        keywords_lower = keywords.lower()
        
        for job in mock_jobs:
            if any(keyword in job['title'].lower() or keyword in job['description'].lower() 
                   for keyword in keywords_lower.split()):
                filtered_jobs.append(job)
        
        return filtered_jobs[:limit] if filtered_jobs else mock_jobs[:limit]
    
    def get_job_details(self, job_url: str) -> Optional[Dict]:
        """Return mock job details."""
        return self.search_jobs("engineer", limit=1)[0]


