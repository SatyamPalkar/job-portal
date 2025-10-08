# Resume Optimizer SaaS - Quick Start Guide

## What This Application Does

This is a **fully functional SaaS application** that helps job seekers optimize their resumes for specific job postings using AI. Here's what it can do:

✅ **Job Search**: Browse and search LinkedIn jobs (mock data in dev mode)  
✅ **Resume Upload**: Upload resumes in PDF, DOCX, or TXT format  
✅ **AI Optimization**: Automatically optimize resumes for specific jobs using GPT-4  
✅ **Match Scoring**: Calculate how well your resume matches each job (0-100%)  
✅ **Smart Analysis**: Extract keywords, required skills, and action words from job descriptions  
✅ **Cover Letters**: Generate AI-powered cover letters  
✅ **Multiple Formats**: Export resumes as PDF, DOCX, or TXT  
✅ **Application Tracking**: Track all your applications in one place  
✅ **User Authentication**: Secure login and account management  

## Quick Start (3 Commands)

### 1. Run Setup Script
```bash
chmod +x setup.sh && ./setup.sh
```

### 2. Add Your Hugging Face API Key (Optional but Recommended)
Edit `.env` file and add:
```
HUGGINGFACE_API_KEY="hf_your_key_here"
```
*Get a FREE API key from https://huggingface.co/settings/tokens*
*(Without this, the app will use mock optimization)*

### 3. Start the Application

**Terminal 1 - Backend:**
```bash
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```

**Open Browser:** http://localhost:3000

## First Use

1. **Register**: Create an account at http://localhost:3000/register
2. **Upload Resume**: Go to "Resumes" → "Upload Resume"
3. **Search Jobs**: Go to "Jobs" → Enter keywords like "Software Engineer"
4. **Optimize**: Click on a job → Select your resume → "Optimize Resume & Apply"
5. **View Results**: Check "Applications" to see your match score and download optimized resume

## What Gets Installed

### Backend (Python)
- FastAPI web framework
- SQLAlchemy for database
- Hugging Face for AI optimization (FREE!)
- Selenium for job scraping
- Spacy for NLP
- ReportLab & python-docx for document generation

### Frontend (React)
- React 18 with TypeScript
- Vite for fast development
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls

## Project Structure

```
Job-application-portal/
├── backend/              # FastAPI backend
│   ├── api/             # REST API routes
│   ├── models/          # Database models
│   ├── services/        # Business logic
│   └── main.py          # App entry point
├── frontend/            # React frontend
│   ├── src/
│   │   ├── pages/      # Application pages
│   │   ├── components/ # Reusable components
│   │   └── services/   # API integration
│   └── package.json
├── requirements.txt     # Python dependencies
├── setup.sh            # Automated setup
└── README.md           # Documentation
```

## Key Features

### 🎯 Resume Optimization
The AI analyzes both your resume and the job description to:
- Add relevant keywords that ATS systems look for
- Replace weak words with strong action verbs
- Highlight matching skills and experience
- Suggest improvements to increase your match score

### 📊 Match Scoring
Get a percentage score (0-100%) showing how well your resume matches each job:
- 80-100%: Excellent match
- 60-79%: Good match
- Below 60%: Consider optimization

### 🔍 Job Analysis
Automatically extracts from job descriptions:
- Required vs. preferred skills
- Technical skills needed
- Soft skills wanted
- Experience level required
- Key action words used

### 📄 Document Generation
Export your optimized resume in:
- **PDF**: For online applications
- **DOCX**: For easy editing
- **TXT**: For ATS systems

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.10+ |
| Database | SQLite (dev) / PostgreSQL (prod) |
| AI | Hugging Face (Mistral-7B / Llama-2) |
| Auth | JWT tokens |
| NLP | Spacy, NLTK |

## Common Issues

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Cannot connect to API"
Make sure backend is running on port 8000

### "No jobs found"
The app uses mock data in development. Click "Search Jobs" to load sample jobs.

### "Optimization not working"
Add your Hugging Face API key to `.env` file. Without it, the app uses basic mock optimization.

## Next Steps

1. **Get Hugging Face API Key (FREE)**: https://huggingface.co/settings/tokens
2. **Read Full Documentation**: See `SETUP_GUIDE.md`
3. **Customize**: Modify the code to fit your needs
4. **Deploy**: Use Heroku/Railway for backend, Vercel/Netlify for frontend

## Cost Considerations

### Hugging Face API
- **FREE tier available!** Includes thousands of requests per month
- No credit card required for the free tier
- Inference API for popular models is completely free
- Upgrade to PRO ($9/month) for faster inference and higher rate limits

### Free Tier Usage
You can use the app with Hugging Face's free tier - it provides real AI optimization at no cost!

## Security Note

⚠️ **Before deploying to production:**
1. Change `SECRET_KEY` in `.env`
2. Use PostgreSQL instead of SQLite
3. Enable HTTPS
4. Never commit API keys to git

## Support

Need help?
- Check `SETUP_GUIDE.md` for detailed instructions
- Review API docs at `/docs`
- Check console logs for errors

---

**Happy Job Hunting! 🚀**

