# 🎯 START HERE - Run in One Command

## Quickest Way to Run

```bash
./run.sh
```

**That's it!** This single command will:
- ✅ Install all dependencies (first time only)
- ✅ Set up the database
- ✅ Start both backend and frontend
- ✅ Open automatically in your browser

## First Time Running?

The script will pause and ask you to get a FREE API key:

1. **Go to**: https://huggingface.co/settings/tokens
2. **Click**: "New token" → Select "Read" → Copy
3. **Edit**: `.env` file and add: `HUGGINGFACE_API_KEY="hf_..."`
4. **Run**: `./run.sh` again

**Or skip this** and the app will use mock data (limited features).

## Access the Application

Once running:
- 🌐 **Frontend**: http://localhost:3000
- 📡 **API Docs**: http://localhost:8000/docs
- 📝 **Logs**: Check `logs/` folder

## Stop the Application

```bash
./stop.sh
```

Or press **Ctrl+C** in the terminal where `run.sh` is running.

## What You Can Do

1. **Register** a new account
2. **Upload** your resume (PDF, DOCX, or TXT)
3. **Search** for jobs (mock data included)
4. **Optimize** your resume for specific jobs
5. **Download** optimized resumes in any format
6. **Track** all your applications

## Need Help?

- 📖 **Quick Guide**: `GET_STARTED.md`
- 🔑 **API Key Help**: `HUGGINGFACE_SETUP.md`
- 📚 **Full Docs**: `SETUP_GUIDE.md`
- ❓ **Troubleshooting**: `QUICKSTART.md`

## Common Commands

```bash
# Run everything
./run.sh

# Stop everything
./stop.sh

# View backend logs
tail -f logs/backend.log

# View frontend logs
tail -f logs/frontend.log
```

---

**Ready?** Just run: `./run.sh` 🚀

