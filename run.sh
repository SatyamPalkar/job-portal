#!/bin/bash

echo "🚀 Resume Optimizer - One-Click Setup & Run"
echo "=========================================="
echo ""

# Initialize pyenv if available
if command -v pyenv &> /dev/null; then
    eval "$(pyenv init -)"
fi

# Check if already set up
if [ ! -d "venv" ]; then
    echo "📦 First-time setup detected. Installing dependencies..."
    echo ""
    
    # Create virtual environment with Python 3.11.4
    echo "Creating Python virtual environment with Python 3.11.4..."
    python -m venv venv
    
    # Activate and install
    source venv/bin/activate
    echo "Installing Python packages (this may take 2-3 minutes)..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Create directories
    mkdir -p uploads/resumes generated_resumes logs
    
    # Create .env if not exists
    if [ ! -f .env ]; then
        cp env.example .env
        echo ""
        echo "⚠️  IMPORTANT: Get your FREE Hugging Face API key!"
        echo "   1. Go to: https://huggingface.co/settings/tokens"
        echo "   2. Click 'New token' → Select 'Read' → Copy token"
        echo "   3. Edit .env file and add: HUGGINGFACE_API_KEY=\"hf_your_token\""
        echo ""
        echo "   Without API key, the app will use mock optimization."
        echo ""
        read -p "Press Enter to continue (or Ctrl+C to exit and add API key first)..."
    fi
    
    # Setup frontend
    if [ ! -d "frontend/node_modules" ]; then
        echo "Installing frontend dependencies..."
        cd frontend
        npm install -q
        cd ..
    fi
    
    echo ""
    echo "✅ Setup complete!"
    echo ""
fi

# Initialize pyenv if available
if command -v pyenv &> /dev/null; then
    eval "$(pyenv init -)"
fi

# Activate virtual environment
source venv/bin/activate

# Start backend in background
echo "🔧 Starting backend server..."
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "   Waiting for backend to initialize..."
sleep 3

# Start frontend in background
echo "🎨 Starting frontend server..."
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo "   Frontend PID: $FRONTEND_PID"

# Wait a bit for frontend to start
sleep 2

echo ""
echo "✅ Application is running!"
echo ""
echo "📱 Open in your browser:"
echo "   👉 http://localhost:3000"
echo ""
echo "📊 API Documentation:"
echo "   👉 http://localhost:8000/docs"
echo ""
echo "📝 View logs:"
echo "   Backend:  tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo "⚠️  To stop the application:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   or press Ctrl+C and run: pkill -f 'uvicorn\|vite'"
echo ""
echo "Press Ctrl+C to stop all servers..."
echo ""

# Save PIDs to file for easy cleanup
echo "$BACKEND_PID" > .pids
echo "$FRONTEND_PID" >> .pids

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f .pids; echo 'Done!'; exit 0" INT

# Keep script running
wait

