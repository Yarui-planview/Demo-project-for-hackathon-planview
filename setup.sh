#!/bin/bash

# Music Library Setup Script
echo "🎵 Setting up Music Library Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Backend setup
echo "🐍 Setting up Python backend..."
cd "$PROJECT_DIR/backend"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Backend setup complete"

# Frontend setup
echo "⚛️ Setting up React frontend..."
cd "$PROJECT_DIR/frontend"

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To run the application:"
echo "1. Start the backend server:"
echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000"
echo ""
echo "2. In another terminal, start the frontend:"
echo "   cd frontend && npm run dev"
echo ""
echo "3. Open http://localhost:5173 in your browser"
echo ""
echo "API documentation will be available at http://localhost:8000/docs"
