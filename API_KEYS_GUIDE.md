# API Keys Setup Guide - Get Everything FREE!

## Required API Key (Already Done ✅)

### Hugging Face (AI Optimization)
- ✅ **Status**: Already configured
- 🔑 **Your Key**: Added to `.env`
- 📝 **Purpose**: Resume optimization, cover letter generation

## Optional API Keys (For Enhanced Features)

### 1. Jooble API (Real Jobs) - FREE 🎉

**What it does**: Fetches real job postings from millions of companies

**Get your FREE key:**
1. Go to: https://jooble.org/api/about
2. Fill out the request form:
   - Name: Satyam Palkar
   - Email: satyampalkar7@gmail.com
   - Website: (can leave blank or use your portfolio)
   - Purpose: "Resume optimization SaaS for personal use"
3. Submit and wait for email (usually within 24 hours)
4. Copy the API key from email
5. Add to `.env`: `JOOBLE_API_KEY="your-key-here"`

**Benefits:**
- Millions of job listings
- Global coverage
- Real-time data
- Completely free

---

### 2. Adzuna API (Real Jobs) - FREE 🎉

**What it does**: Fetches job postings with salary information

**Get your FREE key:**
1. Go to: https://developer.adzuna.com/
2. Click "Get API Key"
3. Sign up with your email
4. Go to dashboard and create new app
5. Copy both App ID and API Key
6. Add to `.env`:
   ```
   ADZUNA_APP_ID="your-app-id"
   ADZUNA_API_KEY="your-api-key"
   ```

**Benefits:**
- 5,000 API calls/month FREE
- Salary information included
- US, UK, Canada, Australia coverage
- Job analytics

---

## Current Status

| API | Status | Purpose |
|-----|--------|---------|
| Hugging Face | ✅ Configured | AI optimization |
| Jooble | ⚪ Optional | Real job listings |
| Adzuna | ⚪ Optional | Real job listings with salary |

## What Works Now

### Without Optional APIs:
- ✅ AI resume optimization (Hugging Face)
- ✅ Mock job data (3 sample jobs)
- ✅ Resume parsing
- ✅ Match scoring
- ✅ Cover letter generation
- ✅ Application tracking

### With Jooble/Adzuna APIs:
- ✅ **Real job listings** from thousands of companies
- ✅ **Fresh data** updated in real-time
- ✅ **Salary information** (Adzuna)
- ✅ **Global coverage** across multiple countries
- ✅ **Automated fetching** every 6 hours (if scheduler enabled)

## How to Enable

### 1. Add API Keys to `.env`

```env
# Copy this to your .env file and fill in the keys

# Jooble (get from https://jooble.org/api/about)
JOOBLE_API_KEY="your-jooble-key"

# Adzuna (get from https://developer.adzuna.com/)
ADZUNA_APP_ID="your-app-id"
ADZUNA_API_KEY="your-api-key"
ADZUNA_COUNTRY="us"  # us, gb, ca, au, etc.
```

### 2. Restart the Backend

```bash
pkill -f uvicorn
./start_backend.sh
```

### 3. Test It

1. Go to http://localhost:3000/jobs
2. Search for "Software Engineer"
3. You should now see REAL jobs instead of mock data!

## Automation Features

### Auto-Apply (Optional)

**Enable in `.env`:**
```env
AUTO_APPLY_ENABLED=true
LINKEDIN_EMAIL="your-email@example.com"
LINKEDIN_PASSWORD="your-password"
```

**Features:**
- Auto-fills application forms
- Uploads resume
- Adds cover letter
- **Safety**: Stops before submission (manual review)
- **Rate limit**: 50 applications/day
- **Human-like**: 20-90 second delays

### Job Scheduler (Optional)

**Enable in `.env`:**
```env
ENABLE_JOB_SCHEDULER=true
```

**Features:**
- Fetches jobs every 6 hours
- Based on your target roles
- Automatic job analysis
- Cleans old jobs daily

## API Rate Limits

| API | Free Tier Limit | Reset Period |
|-----|----------------|--------------|
| Hugging Face | Thousands/month | Monthly |
| Jooble | Check terms | Daily |
| Adzuna | 5,000 calls/month | Monthly |
| Auto-Apply | 50 applications/day | Daily |

## Testing Without Real APIs

You can test all features without API keys:
- Mock job data works perfectly
- All optimization features available
- Good for development and testing

Add real APIs when you're ready to find actual jobs!

## Troubleshooting

### "No jobs found"
- Check if API keys are in `.env`
- Restart backend after adding keys
- Check logs: `tail -f logs/backend.log`

### "API key invalid"
- Verify you copied the complete key
- Check for extra spaces
- Regenerate key if needed

### Jobs still showing mock data
- Restart backend: `./stop.sh && ./run.sh`
- Check `.env` file has correct keys
- Look for "Using mock data" in logs

## Quick Commands

```bash
# Check if real APIs are working
tail -f logs/backend.log | grep "Found.*jobs from"

# Should see:
# Found 10 jobs from Jooble
# Found 15 jobs from Adzuna

# Check rate limit status
curl http://localhost:8000/api/jobs/rate-limit/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

**Summary:**
- ✅ Hugging Face: Already working!
- ⚪ Jooble: Optional - get key from https://jooble.org/api/about
- ⚪ Adzuna: Optional - get key from https://developer.adzuna.com/

**The app works great without them, but real jobs make it even better!** 🚀

