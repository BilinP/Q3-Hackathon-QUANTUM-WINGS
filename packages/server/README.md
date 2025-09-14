# Quantum TSP Solver Backend

A Python Flask API that solves the Traveling Salesman Problem (TSP) using quantum optimization with Qiskit's QAOA algorithm.

## Features

- **Quantum Optimization**: Uses QAOA (Quantum Approximate Optimization Algorithm) for TSP solving
- **Airline Economics**: Incorporates fuel costs, ticket prices, and passenger counts
- **REST API**: Flask-based API with CORS support for frontend integration
- **Error Handling**: Comprehensive validation and error handling
- **Configurable**: Environment-based configuration for different deployment scenarios

## Project Structure

```
server/
├── app.py                 # Main Flask application
├── quantum_tsp_solver.py  # Core quantum TSP solving logic
├── config.py             # Configuration management
├── test_solver.py        # Test script for the solver
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Installation

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

**Development mode:**
```bash
python app.py
```

**Production mode with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

The server will start on `http://localhost:5000` by default.

### API Endpoints

#### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "healthy",
  "message": "Quantum TSP Solver API is running"
}
```

#### Solve TSP
```http
POST /solve-tsp
Content-Type: application/json
```

Request body:
```json
{
  "cities": {
    "SFO": [0.0, 0.0],
    "SEA": [1.0, 3.0],
    "DEN": [4.0, 2.5],
    "DFW": [6.0, 0.5]
  },
  "ticket_price_matrix": [
    [0, 200, 180, 220],
    [200, 0, 160, 190],
    [180, 160, 0, 210],
    [220, 190, 210, 0]
  ],
  "passenger_matrix": [
    [0, 90, 120, 150],
    [100, 0, 80, 130],
    [110, 95, 0, 100],
    [140, 120, 105, 0]
  ]
}
```

Response:
```json
{
  "success": true,
  "result": {
    "route_indices": [0, 1, 2, 3],
    "route_labels": ["SFO", "SEA", "DEN", "DFW", "SFO"],
    "total_cost": 12345.67,
    "leg_breakdown": [
      {
        "from": "SFO",
        "to": "SEA",
        "fuel_cost": 1125.0,
        "ticket_revenue": 18000.0,
        "net_cost": -16875.0
      }
    ],
    "optimization_result": {
      "fval": 12345.67,
      "variables": {...}
    },
    "problem_info": {
      "num_cities": 4,
      "fuel_price": 0.9,
      "fuel_burn_per_km": 2.5,
      "distance_scale": 500
    }
  }
}
```

### Testing

Run the test script to verify everything works:

```bash
python test_solver.py
```

This will:
1. Test the quantum TSP solver with sample data
2. Verify API format compatibility
3. Display detailed results

## Algorithm Details

### Problem Formulation

The solver optimizes airline route profitability by:

1. **Distance Calculation**: Uses Euclidean distance between city coordinates
2. **Cost Modeling**: 
   - Fuel cost = fuel_price × fuel_burn_per_km × distance
   - Revenue = ticket_price × passenger_count
   - Net cost = fuel_cost - revenue
3. **Optimization**: Finds the route that minimizes total net cost

### Quantum Optimization

- **Algorithm**: QAOA (Quantum Approximate Optimization Algorithm)
- **Backend**: Qiskit Aer Simulator
- **Optimizer**: COBYLA with configurable iterations
- **Representation**: Problem converted to QUBO (Quadratic Unconstrained Binary Optimization)

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Flask Configuration
FLASK_ENV=development
PORT=5000

# Quantum TSP Solver Parameters
FUEL_PRICE=0.9
FUEL_BURN_PER_KM=2.5
DISTANCE_SCALE=500
QAOA_REPS=2
MAX_ITER=150

# Logging
LOG_LEVEL=INFO
```

### Default Parameters

- **Fuel Price**: $0.9 per kg
- **Fuel Burn Rate**: 2.5 kg per km per flight
- **Distance Scale**: 500 (multiplier for coordinate-to-km conversion)
- **QAOA Repetitions**: 2
- **Max Optimizer Iterations**: 150

## Error Handling

The API includes comprehensive error handling for:

- Invalid JSON format
- Missing required fields
- Invalid data types
- Matrix dimension mismatches
- Quantum optimization failures

## Dependencies

- **Flask**: Web framework
- **Qiskit**: Quantum computing framework
- **NumPy**: Numerical computations
- **Flask-CORS**: Cross-origin resource sharing
- **python-dotenv**: Environment variable management

## Development

### Adding New Features

1. Extend the `QuantumTSPSolver` class in `quantum_tsp_solver.py`
2. Add new API endpoints in `app.py`
3. Update configuration in `config.py`
4. Add tests in `test_solver.py`

### Debugging

Enable debug mode by setting `FLASK_ENV=development` or running:
```bash
export FLASK_ENV=development
python app.py
```

Logs will show detailed information about the optimization process.

## Performance Notes

- QAOA optimization can take 10-60 seconds depending on problem size
- Consider increasing `MAX_ITER` for better solutions at the cost of longer runtime
- For production, use multiple Gunicorn workers to handle concurrent requests

## License

This project is part of a quantum hackathon submission.
