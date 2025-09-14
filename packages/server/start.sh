#!/bin/bash

# Quantum TSP Solver Backend Startup Script

echo "🚀 Starting Quantum TSP Solver Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📋 Installing dependencies..."
pip install -r requirements.txt

# Run tests to verify everything works
echo "🧪 Running tests..."
python test_solver.py

if [ $? -eq 0 ]; then
    echo "✅ Tests passed! Starting server..."
    
    # Set development environment if not specified
    export FLASK_ENV=${FLASK_ENV:-development}
    
    # Start the server
    echo "🌐 Server starting at http://localhost:5000"
    python app.py
else
    echo "❌ Tests failed! Please check the setup."
    exit 1
fi
