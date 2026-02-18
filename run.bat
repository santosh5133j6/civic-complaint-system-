@echo off
echo ========================================
echo Civic Issue Reporting System - Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if dependencies are installed
echo Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
    echo Downloading NLTK data...
    python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
    echo.
)

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your Supabase credentials.
    echo.
    pause
    exit /b 1
)

REM Create necessary directories
if not exist "static\uploads\" mkdir "static\uploads"
if not exist "models\" mkdir "models"

echo Starting application...
echo.
echo Application will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
