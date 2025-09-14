@echo off
echo 🚀 Starting Basic TSP Solver Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install basic dependencies
echo 📋 Installing basic dependencies...
call install_deps.bat

REM Start the basic server
echo 🌐 Starting basic server at http://localhost:5000
echo ℹ️ Note: Running in mock mode (no quantum optimization)
python app_basic.py

pause
