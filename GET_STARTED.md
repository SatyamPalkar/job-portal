# 🚀 Get Started with Resume Optimizer (FREE!)

## What is This?

An AI-powered SaaS app that optimizes your resume for specific jobs using **FREE** Hugging Face AI models. No credit card needed!

## Quick Start (3 Steps)

### 1️⃣ Run Setup
```bash
chmod +x setup.sh && ./setup.sh
```

### 2️⃣ Get FREE API Key (2 minutes)
1. Go to: **https://huggingface.co/join** (sign up - free!)
2. Go to: **https://huggingface.co/settings/tokens**
3. Click "New token" → Select "Read" → Copy token
4. Edit `.env` file: `HUGGINGFACE_API_KEY="hf_paste_here"`

### 3️⃣ Start the App
```bash
# Terminal 1
./start_backend.sh

# Terminal 2 (new terminal)
./start_frontend.sh

# Open: http://localhost:3000
```

## What You Get

✅ **FREE AI optimization** using Mistral-7B or Llama-2  
✅ **Job search** (LinkedIn-style job listings)  
✅ **Resume parser** (PDF, DOCX, TXT)  
✅ **Match scoring** (0-100% compatibility)  
✅ **Cover letters** (AI-generated)  
✅ **Multiple formats** (PDF, DOCX, TXT export)  
✅ **Application tracking** (manage all your applications)  

## Why Hugging Face?

| Feature | This App (Hugging Face) | OpenAI Alternative |
|---------|------------------------|-------------------|
| Cost | **FREE** 🎉 | $20-50/month |
| Setup | No credit card | Requires payment |
| Quality | Very Good | Excellent |
| Rate Limit | Thousands/month free | Pay per use |

## First Time Usage

1. **Register** at http://localhost:3000/register
2. **Upload Resume** → Go to "Resumes" → Upload your resume
3. **Search Jobs** → Go to "Jobs" → Search for "Software Engineer"
4. **Optimize** → Click a job → Select resume → "Optimize & Apply"
5. **Download** → Go to "Applications" → Download optimized resume

## Without API Key?

The app works without an API key but with limited features:
- ❌ No AI optimization
- ✅ Resume parsing works
- ✅ Job search works
- ✅ Manual editing works

**Get the FREE API key for full features!**

## Files You Need

```
Job-application-portal/
├── .env                 # ⚠️ Add your API key here!
├── setup.sh             # Run this first
├── start_backend.sh     # Start server
├── start_frontend.sh    # Start UI
└── HUGGINGFACE_SETUP.md # Detailed guide
```

## Helpful Links

- 🔑 **Get API Key**: https://huggingface.co/settings/tokens
- 📚 **Detailed Guide**: See `HUGGINGFACE_SETUP.md`
- 📖 **Full Docs**: See `SETUP_GUIDE.md`
- 🐛 **Troubleshooting**: See `QUICKSTART.md`

## Common Issues

**"Cannot connect to API"**
→ Make sure backend is running on port 8000

**"Optimization not working"**
→ Add your Hugging Face API key to `.env`

**"Module not found"**
→ Run: `source venv/bin/activate && pip install -r requirements.txt`

## Need Help?

1. Check `HUGGINGFACE_SETUP.md` for API key setup
2. Check `QUICKSTART.md` for common issues
3. Check `SETUP_GUIDE.md` for detailed setup

---

**Ready?** Run `./setup.sh` and start optimizing! 🚀

**Questions?** All documentation is in the project folder.


