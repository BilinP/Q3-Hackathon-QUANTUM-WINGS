@echo off
REM Quantum TSP Solver Backend Startup Script for Windows

echo 🚀 Starting Quantum TSP Solver Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo 📋 Installing dependencies...
pip install -r requirements.txt

REM Run tests to verify everything works
echo 🧪 Running tests...
python test_solver.py

if %errorlevel% equ 0 (
    echo ✅ Tests passed! Starting server...
    
    REM Set development environment if not specified
    if not defined FLASK_ENV set FLASK_ENV=development
    
    REM Start the server
    echo 🌐 Server starting at http://localhost:5000
    python app.py
) else (
    echo ❌ Tests failed! Please check the setup.
    pause
    exit /b 1
)
