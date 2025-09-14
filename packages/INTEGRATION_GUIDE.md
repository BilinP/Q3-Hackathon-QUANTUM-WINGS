# Frontend-Backend Integration Guide

This guide explains how to run both the frontend and backend together for full quantum TSP optimization.

## 🚀 Quick Start

### Step 1: Start the Backend Server

1. **Open Terminal/Command Prompt** in the `server` folder:
   ```bash
   cd app/packages/server
   ```

2. **Start the Python backend**:
   ```bash
   # Option 1: Using startup script (recommended)
   ./start.sh          # Linux/Mac
   start.bat           # Windows
   
   # Option 2: Manual setup
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

3. **Verify backend is running**:
   - You should see: `Starting Quantum TSP Solver API on port 5000`
   - Test: Open http://localhost:5000/health in browser
   - Should return: `{"status": "healthy", "message": "Quantum TSP Solver API is running"}`

### Step 2: Start the Frontend

1. **Open a NEW Terminal/Command Prompt** in the `client` folder:
   ```bash
   cd app/packages/client
   ```

2. **Start the React frontend**:
   ```bash
   npm install  # First time only
   npm run dev
   ```

3. **Access the application**:
   - Open http://localhost:5173 in your browser
   - You should see the "City Location Input" page

## 🧪 Testing the Integration

### Test Case 1: Basic Integration Test

1. **Add Cities** (on first page):
   - Location 1: Name="SFO", X=0, Y=0
   - Location 2: Name="SEA", X=1, Y=3
   - Location 3: Name="DEN", X=4, Y=2.5
   - Location 4: Name="DFW", X=6, Y=0.5
   - Click "Add City" to add more locations
   - Click "Next" button

2. **Configure Routes** (on second page):
   - You'll see all possible routes between cities
   - Add ticket prices and passenger counts for some routes
   - Example values:
     - SFO → SEA: Ticket Price=200, Passengers=90
     - SEA → DEN: Ticket Price=160, Passengers=80
     - DEN → DFW: Ticket Price=210, Passengers=100
     - DFW → SFO: Ticket Price=220, Passengers=140

3. **Run Quantum Optimization**:
   - Click the "Run" button
   - Wait 10-60 seconds for quantum optimization
   - Check results in the alert dialog and browser console

### Expected Results

**Success Case:**
- Alert shows: "🎉 Quantum optimization completed successfully!"
- Console shows detailed route breakdown
- Best route displayed (e.g., "SFO → SEA → DEN → DFW → SFO")
- Total cost calculated

**Error Cases:**

1. **Backend Not Running:**
   - Alert: "🔌 Connection Error! Cannot connect to the backend server"
   - Solution: Start the Python backend server

2. **Invalid Data:**
   - Alert: "❌ Quantum Optimization Error!"
   - Check console for specific error details

## 🔧 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'qiskit'`
**Solution**: 
```bash
cd server
pip install -r requirements.txt
```

**Problem**: `Port 5000 already in use`
**Solution**: 
```bash
export PORT=5001  # Linux/Mac
set PORT=5001     # Windows
python app.py
```
Then update frontend API_BASE_URL to `http://localhost:5001`

**Problem**: CORS errors in browser
**Solution**: Backend already includes CORS support, but ensure it's running on localhost:5000

### Frontend Issues

**Problem**: `npm run dev` fails
**Solution**:
```bash
cd client
npm install
npm run dev
```

**Problem**: "Network Error" when clicking Run
**Solution**: 
1. Check if backend is running: http://localhost:5000/health
2. Check browser console for specific error
3. Ensure no firewall blocking localhost connections

## 📊 Data Flow Verification

### 1. Frontend Data Formatting
Check browser console after clicking "Run":
```
=== FORMATTED DATA FOR BACKEND ===
cities = {
    "SFO": (0, 0),
    "SEA": (1, 3),
    ...
}
```

### 2. Backend Processing
Check backend terminal output:
```
INFO - Received TSP problem with 4 cities
INFO - Starting quantum optimization...
INFO - Optimization completed. Total cost: $-12345.67
```

### 3. Results Display
Check browser alert and console:
```
✅ Quantum TSP Optimization Results:
Best route: SFO -> SEA -> DEN -> DFW -> SFO
Total cost: $-12,345.67
```

## 🌐 API Endpoints

### Backend Endpoints
- `GET /health` - Health check
- `POST /solve-tsp` - Quantum TSP optimization

### Frontend Configuration
- API Base URL: `http://localhost:5000`
- Timeout: Default fetch timeout (no custom timeout set)
- CORS: Handled by backend

## 📝 Development Notes

### Making Changes

**Backend Changes:**
1. Modify Python files in `server/` folder
2. Restart the backend server
3. Test with frontend

**Frontend Changes:**
1. Modify TypeScript/React files in `client/src/` folder
2. Vite will auto-reload the page
3. Test the integration

### Performance Expectations

- **Quantum Optimization Time**: 10-60 seconds depending on problem size
- **Network Latency**: < 1 second for API calls
- **Total Processing Time**: Usually 15-90 seconds from "Run" click to results

### Scaling Considerations

- **More Cities**: Exponentially increases optimization time
- **Concurrent Users**: Backend supports multiple simultaneous requests
- **Production Deployment**: Use Gunicorn for backend, build client for production

## ✅ Integration Checklist

Before reporting issues, verify:

- [ ] Backend server is running on http://localhost:5000
- [ ] Frontend is running on http://localhost:5173
- [ ] Health check endpoint returns success
- [ ] Browser console shows no CORS errors
- [ ] At least 2 cities entered with valid coordinates
- [ ] At least one route has ticket price and passenger data
- [ ] No firewall/antivirus blocking local connections
- [ ] Python virtual environment activated with all dependencies installed

## 🎯 Success Criteria

The integration is working correctly when:

1. ✅ You can input city data on the first page
2. ✅ Route configuration page loads with all possible routes
3. ✅ Clicking "Run" shows "🚀 Sending data to quantum TSP solver..." in console
4. ✅ Backend receives and processes the data (check backend terminal)
5. ✅ Quantum optimization completes and returns results
6. ✅ Frontend displays success alert with optimal route
7. ✅ Console shows detailed cost breakdown

If all criteria are met, your quantum TSP optimization system is fully operational! 🎉
