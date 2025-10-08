# Job Application Automation Guide

## Overview

Your Resume Optimizer SaaS now includes powerful automation features:

✅ **Real Job APIs** - Fetch jobs from Jooble + Adzuna  
✅ **Auto-Apply** - Playwright automation for job applications  
✅ **Rate Limiting** - 50 applications/day with 20-90s delays  
✅ **Scheduled Fetching** - Auto-fetch jobs every 6 hours  
✅ **Smart Queue** - Process applications in background  

## Setup

### 1. Install Playwright

```bash
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

### 2. Get FREE API Keys

#### Jooble API (FREE)
1. Go to: https://jooble.org/api/about
2. Fill out the form to request API key
3. You'll receive the key by email
4. Add to `.env`: `JOOBLE_API_KEY="your-key-here"`

#### Adzuna API (FREE)
1. Go to: https://developer.adzuna.com/
2. Sign up for free account
3. Get your App ID and API Key
4. Add to `.env`:
   ```
   ADZUNA_APP_ID="your-app-id"
   ADZUNA_API_KEY="your-api-key"
   ```

### 3. Configure Automation

Edit `.env` file:

```env
# Enable Features
AUTO_APPLY_ENABLED=true
ENABLE_JOB_SCHEDULER=true

# Rate Limiting
DAILY_APPLICATION_LIMIT=50
APPLICATION_DELAY_MIN=20
APPLICATION_DELAY_MAX=90

# Optional: LinkedIn credentials for auto-apply
LINKEDIN_EMAIL="your-email@example.com"
LINKEDIN_PASSWORD="your-password"
```

## Features

### 1. Real Job Fetching

**Without API Keys:**
- Uses mock data (3 sample jobs)
- Good for testing

**With API Keys:**
- Fetches real jobs from Jooble + Adzuna
- Combines results from multiple sources
- Removes duplicates automatically
- Saves to database for later use

**Usage:**
```bash
# In the app, go to Jobs → Enter keywords → Search
# Backend will fetch from real APIs
```

### 2. Auto-Apply Feature

**What It Does:**
- Automatically fills out job application forms
- Uploads your optimized resume
- Adds cover letter if available
- **Does NOT auto-submit** (requires manual review for safety)

**Rate Limiting:**
- Maximum 50 applications per day
- Random delays: 20-90 seconds between applications
- Mimics human behavior
- Resets daily at midnight

**How to Use:**

1. Create an application (optimize resume for a job)
2. Click "Auto-Apply" button
3. Application is queued
4. Background process fills the form
5. Review and manually submit

**API Endpoint:**
```
POST /api/applications/{application_id}/auto-apply
```

**Response:**
```json
{
  "status": "queued",
  "queue_position": 3,
  "daily_limit_remaining": 47
}
```

### 3. Job Scheduler

**What It Does:**
- Automatically fetches jobs every 6 hours
- Fetches based on users' target roles
- Analyzes job descriptions automatically
- Cleans up old jobs (30+ days) daily at 2 AM

**Configuration:**
```env
ENABLE_JOB_SCHEDULER=true
```

**Schedule:**
- Job fetching: Every 6 hours
- Cleanup: Daily at 2:00 AM

**How to Set Target Roles:**

In the future, users can set their preferences. For now, you can manually update the database:

```sql
UPDATE users 
SET target_roles = '["Software Engineer", "Full Stack Developer"]'
WHERE id = 1;
```

### 4. Rate Limiter

**Features:**
- Tracks applications per day
- Enforces 50/day limit
- Automatic daily reset
- Persistent storage (survives restarts)

**Check Status:**
```
GET /api/jobs/rate-limit/status
```

**Response:**
```json
{
  "daily_limit": 50,
  "used_today": 12,
  "remaining_today": 38,
  "can_apply": true
}
```

## API Documentation

### New Endpoints

#### Rate Limit Status
```http
GET /api/jobs/rate-limit/status
Authorization: Bearer <token>
```

#### Auto-Apply to Job
```http
POST /api/applications/{application_id}/auto-apply
Authorization: Bearer <token>
```

#### Queue Status
```http
GET /api/applications/queue/status
Authorization: Bearer <token>
```

## How It Works

### Job Fetching Flow

```
1. Scheduler triggers (every 6 hours)
   ↓
2. Get all active users with target roles
   ↓
3. For each user:
   - Fetch jobs from Jooble API
   - Fetch jobs from Adzuna API
   - Combine and deduplicate
   ↓
4. Analyze each job (extract keywords, skills)
   ↓
5. Save to database
   ↓
6. Users see new jobs in the app
```

### Auto-Apply Flow

```
1. User clicks "Auto-Apply"
   ↓
2. Check rate limit (< 50/day?)
   ↓
3. Generate optimized resume PDF
   ↓
4. Add to application queue
   ↓
5. Queue processor:
   - Open browser (Playwright)
   - Navigate to job
   - Fill application form
   - Upload resume
   - Add cover letter
   - STOP (don't submit - manual review)
   ↓
6. Wait 20-90 seconds (random delay)
   ↓
7. Process next application
```

## Safety Features

### 1. Manual Review
- Auto-fill but don't auto-submit
- Review each application before submitting
- Prevents accidental applications

### 2. Rate Limiting
- Maximum 50 applications/day
- Respects job boards' terms of service
- Mimics human behavior with delays

### 3. Queue System
- Process one application at a time
- Clear error handling
- Resume after crashes

### 4. Logging
- All actions logged
- Track success/failure rates
- Debug issues easily

## Best Practices

### 1. Start Slow
- Test with 5-10 applications first
- Verify resume formatting
- Check application quality

### 2. Review Before Submitting
- Always manually review auto-filled forms
- Verify resume uploaded correctly
- Customize answers if needed

### 3. Diversify Sources
- Use both Jooble and Adzuna
- Different APIs have different jobs
- More opportunities

### 4. Monitor Rate Limits
- Check `/rate-limit/status` regularly
- Plan your applications throughout the day
- Don't hit limits early

### 5. Update Target Roles
- Keep preferences current
- Add new roles as career evolves
- Remove irrelevant roles

## Deployment

### For Render / Railway

1. **Add environment variables** in dashboard:
   ```
   JOOBLE_API_KEY=...
   ADZUNA_APP_ID=...
   ADZUNA_API_KEY=...
   AUTO_APPLY_ENABLED=true
   ENABLE_JOB_SCHEDULER=true
   ```

2. **Cron Setup** (Render):
   - Render automatically runs background workers
   - Scheduler will start with the app

3. **Database**: 
   - Switch to PostgreSQL
   - Update `DATABASE_URL`

### For Local Development

Use the settings in `.env` file. The scheduler runs in the same process as the web server.

## Troubleshooting

### Playwright Not Working

```bash
# Install Playwright browsers
playwright install chromium

# If on Linux, install dependencies
playwright install-deps
```

### API Rate Limits

**Jooble:**
- Free tier: Check their terms
- Solution: Add delays, respect limits

**Adzuna:**
- Free tier: 5,000 requests/month
- Solution: Use pagination wisely

### Applications Not Processing

```bash
# Check queue status
curl http://localhost:8000/api/applications/queue/status

# Check rate limit
curl http://localhost:8000/api/jobs/rate-limit/status

# Check logs
tail -f logs/backend.log
```

### Jobs Not Fetching

1. Verify API keys in `.env`
2. Check scheduler is enabled: `ENABLE_JOB_SCHEDULER=true`
3. Check logs for errors
4. Manually trigger with search endpoint

## Cost Analysis

All features use FREE tiers:

| Service | Cost | Limit |
|---------|------|-------|
| Hugging Face | FREE | Thousands/month |
| Jooble API | FREE | Check terms |
| Adzuna API | FREE | 5,000/month |
| Playwright | FREE | Open source |
| APScheduler | FREE | Open source |

**Total Cost: $0/month** 🎉

## Example Usage

### 1. Enable Everything

```env
# In .env
HUGGINGFACE_API_KEY="hf_..."
JOOBLE_API_KEY="..."
ADZUNA_APP_ID="..."
ADZUNA_API_KEY="..."
AUTO_APPLY_ENABLED=true
ENABLE_JOB_SCHEDULER=true
```

### 2. Set Target Roles

Update user preferences (future feature - will have UI):
```sql
UPDATE users 
SET target_roles = '["Software Engineer", "Backend Developer", "Full Stack Developer"]'
WHERE email = 'your-email@example.com';
```

### 3. Let It Run

The system will:
- Fetch 20 jobs per role every 6 hours
- Show them in your dashboard
- Allow you to optimize and apply
- Auto-apply up to 50 jobs/day (if enabled)

## Monitoring

### View Queue Status

```bash
curl http://localhost:8000/api/applications/queue/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### View Rate Limit

```bash
curl http://localhost:8000/api/jobs/rate-limit/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### View Logs

```bash
# Backend logs
tail -f logs/backend.log | grep -i "scheduler\|auto-apply\|queue"
```

## Security Considerations

⚠️ **Important**:

1. **Never commit credentials** to git
2. **LinkedIn automation** may violate terms of service
3. **Use responsibly** - respect rate limits
4. **Review applications** before submitting
5. **Test thoroughly** before enabling auto-apply

## Future Enhancements

- [ ] UI for setting target roles
- [ ] Email notifications for new matching jobs
- [ ] Success rate tracking
- [ ] A/B testing different resume versions
- [ ] Integration with more job boards
- [ ] Smart application timing
- [ ] Interview scheduling assistance

---

**Ready to automate?** Follow the setup steps above! 🚀

