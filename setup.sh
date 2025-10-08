#!/bin/bash

echo "🚀 Setting up Resume Optimizer SaaS..."
echo ""

# Create virtual environment for backend
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📥 Installing backend dependencies (this may take 2-3 minutes)..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads/resumes
mkdir -p generated_resumes
mkdir -p logs

# Set up frontend
echo "⚛️  Setting up frontend..."
cd frontend

# Install frontend dependencies
echo "📥 Installing frontend dependencies..."
npm install

cd ..

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Add your FREE Hugging Face API key to .env!"
    echo "   Get it here: https://huggingface.co/settings/tokens"
    echo "   See HUGGINGFACE_SETUP.md for detailed instructions"
    echo ""
fi

if [ ! -f frontend/.env ]; then
    echo "📝 Creating frontend .env file..."
    echo "VITE_API_URL=http://localhost:8000/api" > frontend/.env
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend:"
echo "   source venv/bin/activate"
echo "   python -m uvicorn backend.main:app --reload --port 8000"
echo ""
echo "2. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open your browser and navigate to http://localhost:3000"
echo ""
echo "⚠️  Important: Don't forget to add your FREE Hugging Face API key to the .env file!"
echo "   👉 Get it from: https://huggingface.co/settings/tokens"
echo "   📖 Read: HUGGINGFACE_SETUP.md for step-by-step instructions"
echo ""

