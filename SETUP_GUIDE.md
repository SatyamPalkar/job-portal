# Resume Optimizer SaaS - Setup Guide

## Overview

This is a complete SaaS application that helps you optimize your resumes for specific job postings using AI. The application:

- Scrapes LinkedIn job postings (or uses mock data for development)
- Analyzes job descriptions to extract requirements and keywords
- Parses your resume and identifies skills and experience
- Uses AI (Hugging Face models) to optimize your resume for each specific job
- Generates tailored cover letters
- Exports optimized resumes in PDF, DOCX, or TXT format
- Tracks your applications and match scores

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **Hugging Face API**: Resume optimization and cover letter generation (FREE!)
- **Selenium/BeautifulSoup**: Job scraping
- **Spacy/NLTK**: Natural language processing
- **ReportLab/python-docx**: Document generation

### Frontend
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first CSS
- **React Router**: Client-side routing
- **React Query**: Data fetching and caching
- **Axios**: HTTP client

## Prerequisites

1. **Python 3.10 or higher**
   ```bash
   python --version
   ```

2. **Node.js 18 or higher**
   ```bash
   node --version
   ```

3. **Hugging Face API Key** (FREE - recommended)
   - Sign up at https://huggingface.co/join
   - Go to https://huggingface.co/settings/tokens
   - Generate a new access token (read access is sufficient)
   - Without this, the app will use mock optimization

## Installation

### Option 1: Automated Setup (Recommended)

Run the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all backend dependencies
- Install frontend dependencies
- Create necessary directories
- Set up configuration files

### Option 2: Manual Setup

#### Backend Setup

1. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download NLP models:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Create necessary directories:
   ```bash
   mkdir -p uploads/resumes generated_resumes logs
   ```

5. Configure environment:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`
   ```bash
   cp .env.example .env
   ```

#### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file:
   ```bash
   echo "VITE_API_URL=http://localhost:8000/api" > .env
   ```

## Configuration

### Backend Configuration (.env)

Edit the `.env` file in the root directory:

```env
# Hugging Face API Key (FREE - get it from https://huggingface.co/settings/tokens)
HUGGINGFACE_API_KEY="hf_your_api_key_here"

# Optional: Use a different Hugging Face model
# HUGGINGFACE_MODEL="mistralai/Mistral-7B-Instruct-v0.2"  # Default
# HUGGINGFACE_MODEL="meta-llama/Llama-2-7b-chat-hf"       # Alternative

# Database (SQLite for development)
DATABASE_URL="sqlite:///./resume_optimizer.db"

# Security (change in production!)
SECRET_KEY="use-openssl-rand-hex-32-to-generate"

# Optional: LinkedIn API credentials
LINKEDIN_CLIENT_ID=""
LINKEDIN_CLIENT_SECRET=""
```

### Frontend Configuration

The frontend automatically proxies API requests to `http://localhost:8000`.

## Running the Application

### Option 1: Using Scripts

Start both servers with the provided scripts:

**Terminal 1 - Backend:**
```bash
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
python -m uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## Using the Application

### 1. Create an Account

1. Navigate to http://localhost:3000
2. Click "Create an account"
3. Fill in your details
4. You'll be automatically logged in

### 2. Upload Your Resume

1. Go to "Resumes" in the navigation
2. Click "Upload Resume"
3. Enter a title for your resume
4. Select your resume file (PDF, DOCX, or TXT)
5. Click "Upload Resume"

The system will automatically parse your resume and extract:
- Skills and keywords
- Experience and education
- Action words used
- Contact information

### 3. Search for Jobs

1. Go to "Jobs" in the navigation
2. Enter job keywords (e.g., "Software Engineer", "Product Manager")
3. Enter location (optional)
4. Click "Search Jobs"

**Note**: In development mode, the app uses mock job data. For production, you would integrate with LinkedIn's API or use a web scraping service.

### 4. Optimize Your Resume for a Job

1. Click on any job listing to view details
2. Select which resume to optimize
3. Choose optimization level:
   - **Conservative**: Minimal changes, keeps your content mostly intact
   - **Balanced**: Moderate optimization (recommended)
   - **Aggressive**: Maximum optimization for ATS and keyword matching
4. Click "Optimize Resume & Apply"

The AI will:
- Analyze the job description
- Compare it with your resume
- Calculate a match score
- Add relevant keywords and action words
- Rephrase content for better impact
- Highlight relevant projects and experience

### 5. Track Your Applications

1. Go to "Applications" in the navigation
2. View all your applications with:
   - Match scores
   - Application status
   - Optimization suggestions
3. Download optimized resumes in PDF, DOCX, or TXT
4. Generate AI-powered cover letters

### 6. View Dashboard

The dashboard shows:
- Total resumes uploaded
- Available jobs
- Number of applications
- Average match score across all applications

## Features

### AI-Powered Optimization

- **Hugging Face Integration**: Uses powerful open-source models like Mistral-7B or Llama-2 to intelligently optimize resumes
- **FREE API Access**: No credit card required, thousands of free requests per month
- **Keyword Optimization**: Automatically adds relevant keywords from job descriptions
- **ATS-Friendly**: Formats resumes to pass Applicant Tracking Systems
- **Action Word Enhancement**: Replaces weak verbs with strong action words
- **Quantifiable Achievements**: Suggests adding metrics and numbers

### Resume Parser

- Supports PDF, DOCX, and TXT formats
- Extracts structured information:
  - Contact details
  - Summary/Objective
  - Work experience
  - Education
  - Skills
  - Projects
  - Certifications

### Job Analysis

- Extracts required vs. preferred skills
- Identifies technical and soft skills
- Calculates experience requirements
- Finds key phrases and action words

### Match Scoring

- Analyzes resume-job compatibility
- Provides detailed breakdown:
  - Technical skills match (40% weight)
  - Required skills match (30% weight)
  - Soft skills match (15% weight)
  - Action words match (15% weight)
- Suggests improvements to increase match score

### Document Generation

- **PDF Export**: Professional PDF resumes
- **DOCX Export**: Editable Word documents
- **TXT Export**: Plain text format for ATS systems

### Cover Letter Generation

- AI-generated cover letters
- Tailored to specific job and company
- Highlights relevant experience
- Professional tone and formatting

## Development

### Project Structure

```
Job-application-portal/
├── backend/
│   ├── api/
│   │   ├── routes/          # API endpoints
│   │   └── dependencies.py  # Auth dependencies
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database setup
│   │   └── security.py      # Auth & security
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   │   ├── job_scraper.py
│   │   ├── resume_parser.py
│   │   ├── nlp_analyzer.py
│   │   ├── ai_optimizer.py
│   │   └── resume_generator.py
│   └── main.py             # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── context/        # React context
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Utility functions
│   └── package.json
└── requirements.txt
```

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

#### Resumes
- `GET /api/resumes/` - List all resumes
- `GET /api/resumes/{id}` - Get resume by ID
- `POST /api/resumes/` - Create resume
- `POST /api/resumes/upload` - Upload resume file
- `POST /api/resumes/optimize` - Optimize resume for job
- `DELETE /api/resumes/{id}` - Delete resume

#### Jobs
- `POST /api/jobs/search` - Search/scrape jobs
- `GET /api/jobs/` - List all jobs
- `GET /api/jobs/{id}` - Get job by ID
- `GET /api/jobs/{id}/analysis` - Get job analysis
- `DELETE /api/jobs/{id}` - Delete job

#### Applications
- `GET /api/applications/` - List all applications
- `GET /api/applications/{id}` - Get application by ID
- `POST /api/applications/` - Create application
- `PATCH /api/applications/{id}` - Update application
- `POST /api/applications/{id}/generate-cover-letter` - Generate cover letter
- `GET /api/applications/{id}/download/{format}` - Download resume
- `DELETE /api/applications/{id}` - Delete application

### Testing

Run backend tests:
```bash
pytest
```

## Deployment

### Backend Deployment (e.g., Heroku, Railway, Render)

1. Update `DATABASE_URL` to use PostgreSQL
2. Set environment variables
3. Run migrations if using Alembic
4. Deploy with gunicorn:
   ```bash
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Frontend Deployment (e.g., Vercel, Netlify)

1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Deploy the `dist` folder

3. Set environment variable:
   ```
   VITE_API_URL=https://your-backend-url.com/api
   ```

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Database errors:**
```bash
rm resume_optimizer.db  # Delete old database
python -c "from backend.core.database import init_db; init_db()"
```

**Import errors:**
Make sure you're running from the project root:
```bash
python -m uvicorn backend.main:app --reload
```

### Frontend Issues

**"Cannot find module" errors:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**API connection errors:**
- Check that backend is running on port 8000
- Check `frontend/.env` has correct API URL

### OpenAI API Issues

**Rate limit errors:**
- Wait a few minutes between requests
- Consider upgrading your OpenAI plan

**No API key:**
- The app will fall back to mock optimization
- Add your API key to `.env` for full functionality

## Security Considerations

### For Production

1. **Change SECRET_KEY**: Use a strong random key
   ```bash
   openssl rand -hex 32
   ```

2. **Use PostgreSQL**: Replace SQLite with PostgreSQL

3. **Enable HTTPS**: Use SSL certificates

4. **Secure API Keys**: Use environment variables, never commit to git

5. **Rate Limiting**: Add rate limiting to API endpoints

6. **Input Validation**: Already implemented via Pydantic

7. **SQL Injection Protection**: Using SQLAlchemy ORM prevents this

## Future Enhancements

- [ ] Real LinkedIn API integration
- [ ] Support for more job boards (Indeed, Glassdoor)
- [ ] Email notifications for new matching jobs
- [ ] A/B testing different resume versions
- [ ] Analytics dashboard
- [ ] Resume templates library
- [ ] Browser extension for one-click apply
- [ ] Interview preparation based on job description
- [ ] Salary negotiation suggestions

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check application logs in the terminal

## License

MIT License - feel free to use and modify for your needs!

