"""NLP analysis service for job descriptions and resumes."""
import re
import json
from typing import List, Dict, Tuple
from collections import Counter


class NLPAnalyzer:
    """Analyze job descriptions and resumes using NLP techniques."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.action_verbs = [
            'achieved', 'administered', 'analyzed', 'architected', 'automated',
            'built', 'collaborated', 'coordinated', 'created', 'delivered',
            'designed', 'developed', 'directed', 'engineered', 'enhanced',
            'established', 'executed', 'generated', 'implemented', 'improved',
            'increased', 'initiated', 'integrated', 'launched', 'led',
            'maintained', 'managed', 'optimized', 'organized', 'performed',
            'planned', 'produced', 'programmed', 'reduced', 'redesigned',
            'resolved', 'streamlined', 'supported', 'transformed', 'upgraded'
        ]
        
        self.technical_skills = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
            'data science', 'data analysis', 'big data', 'hadoop', 'spark',
            'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'devops',
            'ci/cd', 'git', 'linux', 'bash', 'testing', 'tdd', 'unit testing'
        ]
        
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem-solving', 'analytical',
            'critical thinking', 'creativity', 'adaptability', 'time management',
            'collaboration', 'interpersonal', 'presentation', 'negotiation',
            'decision making', 'conflict resolution', 'mentoring', 'coaching'
        ]
    
    def analyze_job_description(self, description: str) -> Dict:
        """
        Analyze a job description to extract requirements and keywords.
        
        Args:
            description: Job description text
            
        Returns:
            Dictionary with analysis results
        """
        description_lower = description.lower()
        
        # Extract required and preferred skills
        required_skills = self._extract_required_skills(description)
        preferred_skills = self._extract_preferred_skills(description)
        
        # Extract technical skills
        technical_skills = self._extract_skills(description_lower, self.technical_skills)
        
        # Extract soft skills
        soft_skills = self._extract_skills(description_lower, self.soft_skills)
        
        # Extract action words used in JD
        action_words = self._extract_skills(description_lower, self.action_verbs)
        
        # Extract experience requirements
        experience_years = self._extract_experience_years(description)
        
        # Extract education requirements
        education_requirements = self._extract_education(description)
        
        # Extract key phrases (multi-word important terms)
        key_phrases = self._extract_key_phrases(description)
        
        # Calculate keyword frequency
        keywords = technical_skills + soft_skills + action_words
        keyword_freq = Counter(keywords)
        
        return {
            'required_skills': required_skills,
            'preferred_skills': preferred_skills,
            'technical_skills': technical_skills,
            'soft_skills': soft_skills,
            'action_words': action_words,
            'experience_years': experience_years,
            'education_requirements': education_requirements,
            'key_phrases': key_phrases,
            'keyword_frequency': dict(keyword_freq.most_common(20)),
            'all_keywords': list(set(keywords))
        }
    
    def analyze_resume(self, resume_text: str) -> Dict:
        """
        Analyze a resume to extract skills and experience.
        
        Args:
            resume_text: Resume text content
            
        Returns:
            Dictionary with analysis results
        """
        resume_lower = resume_text.lower()
        
        # Extract skills
        technical_skills = self._extract_skills(resume_lower, self.technical_skills)
        soft_skills = self._extract_skills(resume_lower, self.soft_skills)
        
        # Extract action words
        action_words = self._extract_skills(resume_lower, self.action_verbs)
        
        # Extract quantifiable achievements
        achievements = self._extract_achievements(resume_text)
        
        # Calculate keyword density
        keywords = technical_skills + soft_skills + action_words
        keyword_freq = Counter(keywords)
        
        return {
            'technical_skills': technical_skills,
            'soft_skills': soft_skills,
            'action_words': action_words,
            'achievements': achievements,
            'keyword_frequency': dict(keyword_freq.most_common(20)),
            'all_keywords': list(set(keywords))
        }
    
    def calculate_match_score(self, resume_analysis: Dict, job_analysis: Dict) -> Tuple[float, Dict]:
        """
        Calculate how well a resume matches a job description.
        
        Args:
            resume_analysis: Resume analysis results
            job_analysis: Job description analysis results
            
        Returns:
            Tuple of (match_score, detailed_breakdown)
        """
        scores = {}
        
        # Technical skills match
        resume_tech = set(resume_analysis.get('technical_skills', []))
        job_tech = set(job_analysis.get('technical_skills', []))
        if job_tech:
            tech_match = len(resume_tech & job_tech) / len(job_tech)
            scores['technical_skills'] = tech_match * 40  # 40% weight
        else:
            scores['technical_skills'] = 0
        
        # Required skills match
        job_required = set(job_analysis.get('required_skills', []))
        if job_required:
            required_match = len(resume_tech & job_required) / len(job_required)
            scores['required_skills'] = required_match * 30  # 30% weight
        else:
            scores['required_skills'] = 0
        
        # Soft skills match
        resume_soft = set(resume_analysis.get('soft_skills', []))
        job_soft = set(job_analysis.get('soft_skills', []))
        if job_soft:
            soft_match = len(resume_soft & job_soft) / len(job_soft)
            scores['soft_skills'] = soft_match * 15  # 15% weight
        else:
            scores['soft_skills'] = 0
        
        # Action words match
        resume_actions = set(resume_analysis.get('action_words', []))
        job_actions = set(job_analysis.get('action_words', []))
        if job_actions:
            action_match = len(resume_actions & job_actions) / len(job_actions)
            scores['action_words'] = action_match * 15  # 15% weight
        else:
            scores['action_words'] = 0
        
        # Total score
        total_score = sum(scores.values())
        
        # Detailed breakdown
        breakdown = {
            'scores': scores,
            'total_score': round(total_score, 2),
            'missing_required_skills': list(job_required - resume_tech),
            'matching_skills': list(resume_tech & job_tech),
            'missing_action_words': list(job_actions - resume_actions),
        }
        
        return round(total_score, 2), breakdown
    
    def _extract_skills(self, text: str, skill_list: List[str]) -> List[str]:
        """Extract skills from text based on a skill list."""
        found_skills = []
        for skill in skill_list:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.append(skill)
        return found_skills
    
    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills from job description."""
        required_section = ""
        
        # Look for requirements section
        patterns = [
            r'requirements?:(.+?)(?=responsibilities|qualifications|preferred|$)',
            r'required:(.+?)(?=responsibilities|qualifications|preferred|$)',
            r'must have:(.+?)(?=responsibilities|qualifications|preferred|$)',
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match:
                required_section = match.group(1)
                break
        
        if required_section:
            return self._extract_skills(required_section, self.technical_skills)
        return []
    
    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract preferred/optional skills from job description."""
        preferred_section = ""
        
        # Look for preferred section
        patterns = [
            r'preferred:(.+?)(?=responsibilities|requirements|$)',
            r'nice to have:(.+?)(?=responsibilities|requirements|$)',
            r'bonus:(.+?)(?=responsibilities|requirements|$)',
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match:
                preferred_section = match.group(1)
                break
        
        if preferred_section:
            return self._extract_skills(preferred_section, self.technical_skills)
        return []
    
    def _extract_experience_years(self, text: str) -> int:
        """Extract years of experience requirement."""
        pattern = r'(\d+)\+?\s*years?'
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return max([int(m) for m in matches])
        return 0
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education requirements."""
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'bs', 'ms', 'ba', 'ma']
        text_lower = text.lower()
        
        found = []
        for keyword in education_keywords:
            if keyword in text_lower:
                found.append(keyword)
        
        return list(set(found))
    
    def _extract_achievements(self, text: str) -> List[str]:
        """Extract quantifiable achievements from resume."""
        # Look for numbers with percentage or improvement keywords
        patterns = [
            r'(\d+%\s+(?:increase|improvement|reduction|growth))',
            r'(increased\s+\w+\s+by\s+\d+%)',
            r'(reduced\s+\w+\s+by\s+\d+%)',
            r'(improved\s+\w+\s+by\s+\d+%)',
        ]
        
        achievements = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            achievements.extend(matches)
        
        return achievements
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract important multi-word phrases."""
        # Common important phrases in job descriptions
        key_phrases_patterns = [
            'machine learning', 'data science', 'software development',
            'full stack', 'front end', 'back end', 'cloud computing',
            'agile methodology', 'cross-functional team', 'rest api',
            'microservices architecture', 'ci/cd pipeline', 'version control',
            'problem solving', 'team player', 'self-motivated'
        ]
        
        text_lower = text.lower()
        found_phrases = [phrase for phrase in key_phrases_patterns if phrase in text_lower]
        
        return found_phrases


