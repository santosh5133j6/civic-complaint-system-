#!/bin/bash

echo "========================================"
echo "Civic Issue Reporting System - Launcher"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
if ! pip show flask > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
    echo "Downloading NLTK data..."
    python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
    echo ""
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure your Supabase credentials."
    echo ""
    exit 1
fi

# Create necessary directories
mkdir -p static/uploads
mkdir -p models

echo "Starting application..."
echo ""
echo "Application will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

python app.py
