from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import json
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock quantum TSP solver for testing without Qiskit
class MockQuantumTSPSolver:
    """
    Mock TSP Solver for testing without Qiskit dependencies
    """
    
    def __init__(self, fuel_price=0.9, fuel_burn_per_km=2.5, distance_scale=500):
        self.fuel_price = fuel_price
        self.fuel_burn_per_km = fuel_burn_per_km
        self.distance_scale = distance_scale
        logger.info("Initialized Mock Quantum TSP Solver (Qiskit not available)")
    
    def solve(self, cities, ticket_price_matrix, passenger_matrix):
        """
        Mock solve method that returns a simple greedy solution
        """
        try:
            # Validate inputs
            self._validate_inputs(cities, ticket_price_matrix, passenger_matrix)
            
            # Convert inputs to numpy arrays
            ticket_price_matrix = np.array(ticket_price_matrix)
            passenger_matrix = np.array(passenger_matrix)
            
            # Get city labels
            labels = list(cities.keys())
            n = len(labels)
            
            # Convert city coordinates to numpy array
            coords = np.array([cities[city] for city in labels])
            
            # Calculate Euclidean distances and scale to km
            dist = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=2) * self.distance_scale
            
            # Calculate costs
            fuel_cost = self.fuel_price * self.fuel_burn_per_km * dist
            ticket_rev_matrix = ticket_price_matrix * passenger_matrix
            edge_cost = (ticket_rev_matrix - fuel_cost) * -1
            np.fill_diagonal(edge_cost, 0.0)
            
            # Simple greedy solution (nearest neighbor)
            route_indices = self._greedy_tsp(edge_cost)
            route_labels = [labels[i] for i in route_indices] + [labels[route_indices[0]]]
            
            # Compute total net cost of route
            total_cost = 0.0
            for a, b in zip(route_indices, route_indices[1:] + [route_indices[0]]):
                total_cost += edge_cost[a, b]
            
            # Generate leg breakdown
            leg_breakdown = []
            for a, b in zip(route_indices, route_indices[1:] + [route_indices[0]]):
                fc = float(fuel_cost[a, b])
                tr = float(ticket_rev_matrix[a, b])
                nc = float(edge_cost[a, b])
                leg_breakdown.append({
                    'from': labels[a],
                    'to': labels[b],
                    'fuel_cost': round(fc, 2),
                    'ticket_revenue': round(tr, 2),
                    'net_cost': round(nc, 2)
                })
            
            return {
                'route_indices': route_indices,
                'route_labels': route_labels,
                'total_cost': round(float(total_cost), 2),
                'leg_breakdown': leg_breakdown,
                'optimization_result': {
                    'fval': float(total_cost),
                    'variables': None
                },
                'problem_info': {
                    'num_cities': n,
                    'fuel_price': self.fuel_price,
                    'fuel_burn_per_km': self.fuel_burn_per_km,
                    'distance_scale': self.distance_scale,
                    'algorithm': 'Greedy (Mock)'
                }
            }
            
        except Exception as e:
            logger.error(f"Error in mock TSP solving: {str(e)}")
            raise
    
    def _greedy_tsp(self, cost_matrix):
        """Simple greedy TSP solution"""
        n = len(cost_matrix)
        unvisited = set(range(1, n))
        current = 0
        route = [current]
        
        while unvisited:
            next_city = min(unvisited, key=lambda x: cost_matrix[current][x])
            route.append(next_city)
            unvisited.remove(next_city)
            current = next_city
        
        return route
    
    def _validate_inputs(self, cities, ticket_price_matrix, passenger_matrix):
        """Validate input data"""
        if not cities or not isinstance(cities, dict):
            raise ValueError("Cities must be a non-empty dictionary")
        
        n = len(cities)
        if n < 2:
            raise ValueError("At least 2 cities are required")
        
        # Validate coordinates
        for city, coords in cities.items():
            if not isinstance(coords, (list, tuple)) or len(coords) != 2:
                raise ValueError(f"City {city} must have exactly 2 coordinates")
        
        # Validate matrices
        if not isinstance(ticket_price_matrix, list) or len(ticket_price_matrix) != n:
            raise ValueError(f"Ticket price matrix must be {n}x{n}")
        
        if not isinstance(passenger_matrix, list) or len(passenger_matrix) != n:
            raise ValueError(f"Passenger matrix must be {n}x{n}")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'TSP Solver API is running (Mock Mode)',
        'mode': 'mock'
    })

@app.route('/solve-tsp', methods=['POST'])
def solve_tsp():
    """
    Solve TSP using mock optimization (for testing without Qiskit)
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
        
        logger.info(f"Received TSP problem with {len(data['cities'])} cities (Mock Mode)")
        
        # Initialize mock solver
        solver = MockQuantumTSPSolver()
        
        # Solve the TSP problem
        result = solver.solve(
            cities=data['cities'],
            ticket_price_matrix=data['ticket_price_matrix'],
            passenger_matrix=data['passenger_matrix']
        )
        
        logger.info(f"Mock TSP solved. Best route: {result['route_labels']}")
        
        return jsonify({
            'success': True,
            'result': result,
            'mode': 'mock',
            'note': 'This is a mock solution using greedy algorithm. Install Qiskit for quantum optimization.'
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
    
    logger.info(f"Starting TSP Solver API (Mock Mode) on port {port}")
    logger.info("Note: This is running in mock mode. Install Qiskit for quantum features.")
    app.run(host='0.0.0.0', port=port, debug=debug)
