"""Resume parsing service."""
import json
import re
from typing import Dict, List, Optional
from pathlib import Path
import PyPDF2
from docx import Document


class ResumeParser:
    """Parse resumes from various formats and extract structured information."""
    
    def __init__(self):
        """Initialize the parser."""
        self.sections = {
            'summary': ['summary', 'objective', 'profile', 'about'],
            'experience': ['experience', 'work history', 'employment', 'work experience'],
            'education': ['education', 'academic', 'qualification'],
            'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
            'projects': ['projects', 'portfolio', 'work samples'],
            'certifications': ['certifications', 'certificates', 'licenses'],
        }
    
    def parse_file(self, file_path: str) -> Dict:
        """
        Parse a resume file and extract structured information.
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Dictionary with parsed resume data
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.pdf':
            text = self._extract_pdf_text(file_path)
        elif extension == '.docx':
            text = self._extract_docx_text(file_path)
        elif extension == '.txt':
            text = self._extract_txt_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
        
        # Parse the text into sections
        parsed_data = self._parse_text(text)
        parsed_data['raw_text'] = text
        
        return parsed_data
    
    def _extract_pdf_text(self, file_path: Path) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            raise
        
        return text.strip()
    
    def _extract_docx_text(self, file_path: Path) -> str:
        """Extract text from DOCX file."""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    
    def _extract_txt_text(self, file_path: Path) -> str:
        """Extract text from TXT file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    
    def _parse_text(self, text: str) -> Dict:
        """
        Parse resume text into structured sections.
        
        Args:
            text: Raw resume text
            
        Returns:
            Dictionary with parsed sections
        """
        lines = text.split('\n')
        
        # Initialize data structure
        data = {
            'summary': '',
            'experience': [],
            'education': [],
            'skills': [],
            'projects': [],
            'certifications': [],
        }
        
        current_section = None
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line is a section header
            section_found = False
            for section_name, keywords in self.sections.items():
                if any(keyword in line_lower for keyword in keywords):
                    # Save previous section
                    if current_section and current_content:
                        self._save_section(data, current_section, current_content)
                    
                    current_section = section_name
                    current_content = []
                    section_found = True
                    break
            
            if not section_found and line.strip():
                current_content.append(line.strip())
        
        # Save last section
        if current_section and current_content:
            self._save_section(data, current_section, current_content)
        
        # Extract additional information
        data['keywords'] = self._extract_keywords(text)
        data['action_words'] = self._extract_action_words(text)
        data['email'] = self._extract_email(text)
        data['phone'] = self._extract_phone(text)
        
        return data
    
    def _save_section(self, data: Dict, section: str, content: List[str]):
        """Save parsed section content."""
        if section in ['summary']:
            data[section] = ' '.join(content)
        elif section == 'skills':
            # Parse skills (comma or newline separated)
            skills = []
            for line in content:
                skills.extend([s.strip() for s in re.split(r'[,\n]', line) if s.strip()])
            data[section] = skills
        elif section in ['experience', 'education', 'projects', 'certifications']:
            # Parse structured entries
            data[section] = self._parse_entries(content)
        else:
            data[section] = content
    
    def _parse_entries(self, content: List[str]) -> List[Dict]:
        """Parse structured entries like experience or education."""
        entries = []
        current_entry = {'description': []}
        
        for line in content:
            # Check if this is a new entry (heuristic: lines with dates or company names)
            if self._looks_like_entry_header(line):
                if current_entry.get('description'):
                    entries.append(current_entry)
                current_entry = {'title': line, 'description': []}
            else:
                current_entry['description'].append(line)
        
        if current_entry.get('description'):
            entries.append(current_entry)
        
        return entries
    
    def _looks_like_entry_header(self, line: str) -> bool:
        """Check if a line looks like an entry header."""
        # Heuristics for detecting entry headers
        date_pattern = r'\d{4}|\d{1,2}/\d{4}|present|current'
        return bool(re.search(date_pattern, line, re.IGNORECASE))
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from resume."""
        # Simple keyword extraction (in production, use NLP models)
        common_tech_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'node', 'django', 'flask', 'spring', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'sql', 'mongodb', 'postgresql',
            'machine learning', 'ai', 'data science', 'agile', 'scrum',
            'rest api', 'graphql', 'microservices', 'ci/cd', 'git'
        ]
        
        text_lower = text.lower()
        found_keywords = [kw for kw in common_tech_keywords if kw in text_lower]
        
        return found_keywords
    
    def _extract_action_words(self, text: str) -> List[str]:
        """Extract action words/verbs from resume."""
        action_words = [
            'developed', 'designed', 'implemented', 'created', 'built',
            'led', 'managed', 'optimized', 'improved', 'increased',
            'reduced', 'achieved', 'delivered', 'collaborated', 'coordinated',
            'analyzed', 'architected', 'deployed', 'integrated', 'automated'
        ]
        
        text_lower = text.lower()
        found_words = [word for word in action_words if word in text_lower]
        
        return list(set(found_words))
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text."""
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else None
    
    def parse_text_content(self, text: str) -> Dict:
        """
        Parse resume from raw text content.
        
        Args:
            text: Resume text content
            
        Returns:
            Dictionary with parsed resume data
        """
        parsed_data = self._parse_text(text)
        parsed_data['raw_text'] = text
        return parsed_data


