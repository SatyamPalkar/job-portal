# Resume Optimizer SaaS

A powerful SaaS application that reads LinkedIn jobs, analyzes job descriptions, and automatically optimizes your resume with relevant action words and projects to qualify your application.

## Features

### Core Features
- 🔍 **Real Job APIs**: Fetch jobs from Jooble + Adzuna (FREE APIs)
- 🤖 **AI-Powered Analysis**: Uses Hugging Face models (Mistral-7B/Llama-2) to analyze job descriptions
- 📝 **Resume Optimization**: Automatically updates your resume with relevant action words and projects
- 🎯 **Smart Matching**: Matches your experience with job requirements (0-100% score)
- 📄 **Multiple Formats**: Export optimized resumes in PDF, DOCX, and TXT formats
- 🔐 **Secure Authentication**: User accounts with JWT token-based authentication

### Automation Features (NEW!)
- 🤖 **Auto-Apply**: Playwright automation to fill job applications automatically
- ⏰ **Job Scheduler**: Fetch jobs every 6 hours automatically (Cron-based)
- 🚦 **Rate Limiting**: 50 applications/day with 20-90s random delays
- 📊 **Application Queue**: Smart background processing of applications
- 🎯 **Multi-Source**: Combines jobs from Jooble, Adzuna, and mock data
- 📈 **Analytics Dashboard**: Track application success rates and optimization metrics

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database management
- **Hugging Face**: AI-powered text analysis and generation (free API)
- **Selenium/BeautifulSoup**: Web scraping for LinkedIn jobs
- **Spacy/NLTK**: Natural language processing

### Frontend
- **React**: Modern UI library
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Data fetching and caching
- **React Router**: Client-side routing

### Database
- **PostgreSQL**: Production database (SQLite for development)

## Quick Start (One Command!)

```bash
./run.sh
```

This will automatically set up everything and start the application!

See `START_HERE.md` for the simplest way to get started.

## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (optional, SQLite works for dev)

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your Hugging Face API key (FREE!)
# See HUGGINGFACE_SETUP.md for detailed instructions
```

4. Run database migrations:
```bash
cd backend
alembic upgrade head
```

5. Start the backend server:
```bash
uvicorn backend.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Usage

1. **Create an Account**: Sign up with your email
2. **Upload Your Resume**: Upload your current resume (PDF or DOCX)
3. **Set Your Preferences**: Define your target job titles and industries
4. **Search Jobs**: The system will automatically fetch relevant LinkedIn jobs
5. **Analyze & Optimize**: Select a job and let AI optimize your resume
6. **Download**: Get your optimized resume in your preferred format

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Architecture

```
Job-application-portal/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   └── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   │   ├── job_scraper.py
│   │   ├── resume_parser.py
│   │   ├── ai_optimizer.py
│   │   └── resume_generator.py
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
└── requirements.txt
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

