@echo off
echo 🔧 Installing Python dependencies step by step...

REM Upgrade pip first
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install setuptools and wheel first
echo 🛠️ Installing build tools...
pip install setuptools wheel

REM Install basic dependencies first
echo 📋 Installing basic dependencies...
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install numpy>=1.21.0
pip install python-dotenv==1.0.0
pip install gunicorn==21.2.0

echo ✅ Basic dependencies installed successfully!

REM Try to install Qiskit (optional)
echo 🔬 Attempting to install Qiskit (this may take a while)...
pip install qiskit --timeout=300
if %errorlevel% neq 0 (
    echo ⚠️ Qiskit installation failed. You can run the basic server without quantum features.
    goto :end
)

echo 🔬 Installing Qiskit extensions...
pip install qiskit-aer --timeout=300
if %errorlevel% neq 0 (
    echo ⚠️ Qiskit-aer installation failed. Using basic Qiskit only.
    goto :end
)

pip install qiskit-algorithms --timeout=300
pip install qiskit-optimization --timeout=300

:end
echo 🎉 Installation completed!
echo You can now run: python app.py
