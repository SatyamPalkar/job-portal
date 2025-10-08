#!/bin/bash

echo "🚀 Starting Resume Optimizer Backend..."

# Activate virtual environment
source venv/bin/activate

# Start the backend server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000


