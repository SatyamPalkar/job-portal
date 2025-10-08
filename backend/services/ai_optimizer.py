"""AI-powered resume optimizer using Hugging Face API."""
import json
import requests
from typing import Dict, List, Optional
from backend.core.config import settings


class AIResumeOptimizer:
    """Optimize resumes using AI based on job descriptions."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize the optimizer with Hugging Face API key."""
        self.api_key = api_key or settings.HUGGINGFACE_API_KEY
        self.model = model or settings.HUGGINGFACE_MODEL
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        
        if self.api_key:
            self.headers = {"Authorization": f"Bearer {self.api_key}"}
        else:
            self.headers = None
            print("Warning: Hugging Face API key not set. Using mock optimizer.")
    
    def optimize_resume(
        self,
        resume_content: str,
        job_description: str,
        job_analysis: Dict,
        resume_analysis: Dict,
        optimization_level: str = "balanced"
    ) -> Dict:
        """
        Optimize resume content based on job description.
        
        Args:
            resume_content: Original resume content
            job_description: Target job description
            job_analysis: Analyzed job requirements
            resume_analysis: Analyzed resume content
            optimization_level: conservative, balanced, or aggressive
            
        Returns:
            Dictionary with optimized content and suggestions
        """
        if not self.headers:
            return self._mock_optimize(resume_content, job_analysis)
        
        # Prepare optimization instructions based on level
        instructions = self._get_optimization_instructions(optimization_level)
        
        # Identify missing skills and action words
        missing_skills = job_analysis.get('all_keywords', [])
        resume_skills = resume_analysis.get('all_keywords', [])
        gaps = list(set(missing_skills) - set(resume_skills))
        
        # Create the prompt
        prompt = self._create_optimization_prompt(
            resume_content,
            job_description,
            gaps,
            job_analysis,
            instructions
        )
        
        try:
            # Call Hugging Face API
            full_prompt = f"""<s>[INST] You are an expert resume writer and career coach specializing in optimizing resumes for specific job applications. You help candidates highlight their relevant experience and skills while maintaining authenticity.

{prompt} [/INST]</s>"""
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 2000,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                elif isinstance(result, dict):
                    generated_text = result.get('generated_text', '')
                else:
                    generated_text = str(result)
                
                # Parse the AI response
                optimizations = self._parse_ai_response(generated_text)
                
                return {
                    'optimized_content': optimizations.get('optimized_resume', resume_content),
                    'optimizations_applied': optimizations.get('changes', []),
                    'suggested_improvements': optimizations.get('suggestions', []),
                    'action_words_added': optimizations.get('action_words', []),
                }
            else:
                print(f"Hugging Face API error: {response.status_code} - {response.text}")
                return self._mock_optimize(resume_content, job_analysis)
            
        except Exception as e:
            print(f"Error calling Hugging Face API: {e}")
            return self._mock_optimize(resume_content, job_analysis)
    
    def generate_cover_letter(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_title: str
    ) -> str:
        """
        Generate a tailored cover letter.
        
        Args:
            resume_content: Resume content
            job_description: Job description
            company_name: Company name
            job_title: Job title
            
        Returns:
            Generated cover letter
        """
        if not self.headers:
            return self._mock_cover_letter(company_name, job_title)
        
        prompt = f"""
Based on the following resume and job description, write a compelling and professional cover letter.

Resume:
{resume_content[:1500]}

Job Title: {job_title}
Company: {company_name}
Job Description:
{job_description[:1000]}

Write a cover letter that:
1. Shows enthusiasm for the role and company
2. Highlights relevant experience from the resume
3. Demonstrates understanding of job requirements
4. Is concise (3-4 paragraphs)
5. Has a professional tone
6. Includes specific examples where possible
"""
        
        try:
            full_prompt = f"""<s>[INST] You are an expert at writing compelling cover letters that help candidates stand out.

{prompt} [/INST]</s>"""
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 1000,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', self._mock_cover_letter(company_name, job_title))
                elif isinstance(result, dict):
                    return result.get('generated_text', self._mock_cover_letter(company_name, job_title))
                else:
                    return self._mock_cover_letter(company_name, job_title)
            else:
                print(f"Hugging Face API error: {response.status_code}")
                return self._mock_cover_letter(company_name, job_title)
            
        except Exception as e:
            print(f"Error generating cover letter: {e}")
            return self._mock_cover_letter(company_name, job_title)
    
    def suggest_improvements(
        self,
        resume_content: str,
        job_analysis: Dict,
        match_score: float
    ) -> List[Dict]:
        """
        Suggest specific improvements to increase match score.
        
        Args:
            resume_content: Current resume content
            job_analysis: Analyzed job requirements
            match_score: Current match score
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Check for missing required skills
        required_skills = job_analysis.get('required_skills', [])
        for skill in required_skills[:5]:  # Top 5 required skills
            if skill.lower() not in resume_content.lower():
                suggestions.append({
                    'type': 'missing_skill',
                    'priority': 'high',
                    'suggestion': f'Add "{skill}" to your skills or experience section if you have experience with it',
                    'impact': 'Could increase match score by 5-10%'
                })
        
        # Check for missing action words
        action_words = job_analysis.get('action_words', [])
        for word in action_words[:5]:
            if word not in resume_content.lower():
                suggestions.append({
                    'type': 'action_word',
                    'priority': 'medium',
                    'suggestion': f'Consider using the action verb "{word}" to describe your achievements',
                    'impact': 'Improves readability and ATS compatibility'
                })
        
        # Check for quantifiable achievements
        if match_score < 70:
            suggestions.append({
                'type': 'achievement',
                'priority': 'high',
                'suggestion': 'Add quantifiable achievements (e.g., "Increased performance by 30%")',
                'impact': 'Makes your impact more concrete and impressive'
            })
        
        # Check for keywords
        if match_score < 60:
            missing_keywords = set(job_analysis.get('technical_skills', [])) - set(resume_content.lower().split())
            if missing_keywords:
                suggestions.append({
                    'type': 'keywords',
                    'priority': 'high',
                    'suggestion': f'Add these relevant keywords: {", ".join(list(missing_keywords)[:5])}',
                    'impact': 'Improves ATS scan score significantly'
                })
        
        return suggestions
    
    def _get_optimization_instructions(self, level: str) -> str:
        """Get optimization instructions based on level."""
        instructions = {
            'conservative': """
            Make minimal changes:
            - Only add clearly relevant keywords that fit naturally
            - Rephrase existing content for better impact
            - Keep the original structure and most content intact
            """,
            'balanced': """
            Make moderate changes:
            - Add relevant keywords and action words where appropriate
            - Reorganize content to highlight relevant experience
            - Add or enhance bullet points that match job requirements
            - Maintain authenticity while optimizing for the role
            """,
            'aggressive': """
            Make substantial changes:
            - Heavily emphasize experience relevant to the job
            - Add all matching keywords and technical skills
            - Rewrite sections to align closely with job description
            - Focus on maximizing ATS and recruiter appeal
            """
        }
        return instructions.get(level, instructions['balanced'])
    
    def _create_optimization_prompt(
        self,
        resume: str,
        job_desc: str,
        gaps: List[str],
        job_analysis: Dict,
        instructions: str
    ) -> str:
        """Create the optimization prompt for AI."""
        return f"""
Optimize the following resume for this specific job posting.

RESUME:
{resume[:2000]}

JOB DESCRIPTION:
{job_desc[:1500]}

OPTIMIZATION LEVEL:
{instructions}

KEY REQUIREMENTS FROM JOB:
- Required Skills: {', '.join(job_analysis.get('required_skills', [])[:10])}
- Technical Skills: {', '.join(job_analysis.get('technical_skills', [])[:10])}
- Action Words to Use: {', '.join(job_analysis.get('action_words', [])[:10])}

MISSING FROM CURRENT RESUME:
{', '.join(gaps[:15])}

Please provide:
1. An optimized version of the resume
2. A list of specific changes made
3. Additional suggestions for improvement
4. Action words that were added or should be added

Format your response as JSON:
{{
    "optimized_resume": "...",
    "changes": ["change 1", "change 2", ...],
    "suggestions": ["suggestion 1", "suggestion 2", ...],
    "action_words": ["word1", "word2", ...]
}}
"""
    
    def _parse_ai_response(self, response: str) -> Dict:
        """Parse AI response into structured format."""
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except Exception as e:
            print(f"Error parsing AI response: {e}")
        
        # Fallback: return raw response
        return {
            'optimized_resume': response,
            'changes': ['AI optimization applied'],
            'suggestions': [],
            'action_words': []
        }
    
    def _mock_optimize(self, resume_content: str, job_analysis: Dict) -> Dict:
        """Mock optimization for when API is not available."""
        # Simple mock: add missing keywords to skills section
        missing_skills = job_analysis.get('technical_skills', [])[:5]
        
        optimizations = [
            f"Added keyword '{skill}' to skills section" for skill in missing_skills
        ]
        
        suggestions = [
            "Consider adding quantifiable achievements",
            "Use more action verbs like 'implemented', 'optimized', 'led'",
            "Tailor your summary to match the job description",
        ]
        
        return {
            'optimized_content': resume_content + f"\n\nSkills: {', '.join(missing_skills)}",
            'optimizations_applied': optimizations,
            'suggested_improvements': suggestions,
            'action_words_added': ['implemented', 'optimized', 'developed'],
        }
    
    def _mock_cover_letter(self, company_name: str, job_title: str) -> str:
        """Mock cover letter for when API is not available."""
        return f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my background in software development and proven track record of delivering high-quality solutions, I am confident I would be a valuable addition to your team.

Throughout my career, I have developed expertise in modern development technologies and practices. I am particularly excited about this opportunity at {company_name} because of your innovative approach and commitment to excellence.

My experience aligns well with your requirements, and I am eager to contribute to your team's success. I would welcome the opportunity to discuss how my skills and experience can benefit {company_name}.

Thank you for considering my application.

Best regards,
[Your Name]
"""

