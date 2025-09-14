from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
from quantum_tsp_solver import QuantumTSPSolver

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Quantum TSP Solver API is running'
    })

@app.route('/solve-tsp', methods=['POST'])
def solve_tsp():
    """
    Solve TSP using quantum optimization
    Expected JSON payload:
    {
        "cities": {
            "SFO": [0.0, 0.0],
            "SEA": [1.0, 3.0],
            "DEN": [4.0, 2.5],
            "DFW": [6.0, 0.5]
        },
        "ticket_price_matrix": [[0, 200, 180, 220], ...],
        "passenger_matrix": [[0, 90, 120, 150], ...]
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['cities', 'ticket_price_matrix', 'passenger_matrix']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        logger.info(f"Received TSP problem with {len(data['cities'])} cities")
        
        # Initialize solver
        solver = QuantumTSPSolver()
        
        # Solve the TSP problem
        result = solver.solve(
            cities=data['cities'],
            ticket_price_matrix=data['ticket_price_matrix'],
            passenger_matrix=data['passenger_matrix']
        )
        
        logger.info(f"TSP solved successfully. Best route: {result['route_labels']}")
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'error': f'Invalid input data: {str(e)}'}), 400
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error occurred'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Quantum TSP Solver API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
