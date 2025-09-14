# Backend Installation Troubleshooting Guide

## 🚨 Common Issues and Solutions

### Issue 1: Qiskit Installation Fails

**Error**: `BackendUnavailable: Cannot import 'setuptools.build_meta'`

**Quick Solution - Use Basic Mode**:
```bash
cd app/packages/server
start_basic.bat
```

This will run a mock version without quantum features for testing.

**Full Solution**:
1. **Update Python build tools**:
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

2. **Install Visual C++ Build Tools** (Windows):
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "C++ build tools" workload

3. **Try step-by-step installation**:
   ```bash
   pip install -r requirements-simple.txt
   pip install qiskit --timeout=600
   ```

### Issue 2: NumPy Installation Fails

**Error**: `ModuleNotFoundError: No module named 'numpy'`

**Solution**:
```bash
# Activate virtual environment first
venv\Scripts\activate

# Install NumPy specifically
pip install numpy>=1.21.0

# If still fails, try:
pip install --only-binary=all numpy
```

### Issue 3: Virtual Environment Issues

**Error**: Virtual environment not activating properly

**Solution**:
```bash
# Delete old environment
rmdir /s venv

# Create new environment
python -m venv venv

# Activate and install
venv\Scripts\activate
pip install --upgrade pip
```

### Issue 4: Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use different port
set PORT=5001
python app_basic.py
```

## 🛠️ Installation Methods

### Method 1: Basic Mode (Recommended for Testing)
```bash
cd app/packages/server
start_basic.bat
```
- ✅ Quick setup
- ✅ No complex dependencies
- ✅ Works immediately
- ❌ No quantum optimization (uses greedy algorithm)

### Method 2: Manual Step-by-Step
```bash
# 1. Create environment
python -m venv venv
venv\Scripts\activate

# 2. Upgrade tools
python -m pip install --upgrade pip setuptools wheel

# 3. Install basic deps
pip install flask flask-cors numpy python-dotenv gunicorn

# 4. Test basic server
python app_basic.py

# 5. Try quantum deps (optional)
pip install qiskit qiskit-aer qiskit-algorithms qiskit-optimization
python app.py
```

### Method 3: Using Conda (Alternative)
```bash
# Install Anaconda/Miniconda first
conda create -n quantum-tsp python=3.9
conda activate quantum-tsp
conda install numpy flask
pip install flask-cors python-dotenv
pip install qiskit qiskit-aer qiskit-algorithms qiskit-optimization
```

## 🔍 Verification Steps

### 1. Check Python Version
```bash
python --version
# Should be 3.8 or higher
```

### 2. Check Virtual Environment
```bash
# Should show virtual environment path
where python
```

### 3. Test Basic Dependencies
```bash
python -c "import flask, numpy; print('Basic deps OK')"
```

### 4. Test Quantum Dependencies (Optional)
```bash
python -c "import qiskit; print('Qiskit OK')"
```

### 5. Test Server Health
```bash
# After starting server
curl http://localhost:5000/health
# Or open in browser
```

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 2GB available
- **Disk**: 1GB free space
- **OS**: Windows 10/11, macOS 10.15+, or Linux

### For Full Quantum Features
- **Python**: 3.9 recommended
- **RAM**: 4GB available
- **CPU**: Multi-core recommended
- **Build Tools**: Visual C++ (Windows) or GCC (Linux/Mac)

## 🎯 Quick Test Commands

### Test 1: Basic Server
```bash
cd app/packages/server
python app_basic.py
```
Expected: Server starts on port 5000

### Test 2: API Endpoint
```bash
curl -X POST http://localhost:5000/solve-tsp \
  -H "Content-Type: application/json" \
  -d '{
    "cities": {"A": [0,0], "B": [1,1]},
    "ticket_price_matrix": [[0,100],[100,0]],
    "passenger_matrix": [[0,50],[50,0]]
  }'
```
Expected: JSON response with route solution

### Test 3: Frontend Integration
1. Start backend: `python app_basic.py`
2. Start frontend: `cd ../client && npm run dev`
3. Test full workflow in browser

## 🆘 If Nothing Works

### Last Resort Options

1. **Use Online Python Environment**:
   - Google Colab
   - Replit
   - CodePen (for frontend only)

2. **Docker Alternative** (if Docker available):
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements-simple.txt .
   RUN pip install -r requirements-simple.txt
   COPY . .
   CMD ["python", "app_basic.py"]
   ```

3. **Contact Support**:
   - Check GitHub Issues
   - Python community forums
   - Stack Overflow

## 📞 Getting Help

### Include This Information When Asking for Help:
- Python version: `python --version`
- Operating system
- Error messages (full traceback)
- Steps you've already tried
- Virtual environment status

### Useful Debug Commands:
```bash
# System info
python -c "import sys; print(sys.version)"
pip list
pip check

# Environment info
echo %PATH%
echo %VIRTUAL_ENV%
```

Remember: The basic mode (`app_basic.py`) will work for testing the frontend-backend integration even without quantum features! 🚀
