# --- Imports (Qiskit 1.x style) ---
from qiskit_aer import AerSimulator
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler
from qiskit_optimization.applications import Tsp
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo

import numpy as np
import logging

logger = logging.getLogger(__name__)

class QuantumTSPSolver:
    """
    Quantum TSP Solver using QAOA algorithm
    """
    
    def __init__(self, fuel_price=0.9, fuel_burn_per_km=2.5, distance_scale=500, qaoa_reps=2, max_iter=150):
        """
        Initialize the quantum TSP solver
        
        Args:
            fuel_price (float): Price per kg of fuel in $
            fuel_burn_per_km (float): Fuel burn rate in kg per km per flight
            distance_scale (int): Scale factor to convert coordinates to km
            qaoa_reps (int): Number of QAOA repetitions
            max_iter (int): Maximum iterations for optimizer
        """
        self.fuel_price = fuel_price
        self.fuel_burn_per_km = fuel_burn_per_km
        self.distance_scale = distance_scale
        self.qaoa_reps = qaoa_reps
        self.max_iter = max_iter
        
        logger.info(f"Initialized QuantumTSPSolver with fuel_price=${fuel_price}, "
                   f"fuel_burn_per_km={fuel_burn_per_km} kg/km")
    
    def solve(self, cities, ticket_price_matrix, passenger_matrix):
        """
        Solve the TSP problem using quantum optimization
        
        Args:
            cities (dict): Dictionary of city names to coordinate tuples
            ticket_price_matrix (list): 2D list of ticket prices
            passenger_matrix (list): 2D list of passenger counts
            
        Returns:
            dict: Solution containing route, costs, and breakdown
        """
        try:
            # Validate inputs
            self._validate_inputs(cities, ticket_price_matrix, passenger_matrix)
            
            logger.info(f"Starting TSP optimization for {len(cities)} cities")
            
            # Convert inputs to numpy arrays
            ticket_price_matrix = np.array(ticket_price_matrix)
            passenger_matrix = np.array(passenger_matrix)
            
            # Get city labels and coordinates
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
            
            logger.info("Calculated cost matrices")
            
            # Build TSP -> Quadratic Program (QP)
            tsp = Tsp(edge_cost)
            qp = tsp.to_quadratic_program()
            
            # Convert to QUBO (binary form)
            conv = QuadraticProgramToQubo()
            qubo = conv.convert(qp)
            
            logger.info("Converted problem to QUBO format")
            
            # Solve with QAOA on AerSimulator
            sampler = Sampler()
            qaoa = QAOA(sampler=sampler, reps=self.qaoa_reps, optimizer=COBYLA(maxiter=self.max_iter))
            meo = MinimumEigenOptimizer(qaoa)
            
            logger.info("Starting quantum optimization...")
            result = meo.solve(qubo)
            
            # Decode route and report cost
            tsp_solution = tsp.interpret(result)
            route_indices = tsp_solution
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
            
            logger.info(f"Optimization completed. Total cost: ${total_cost:.2f}")
            
            return {
                'route_indices': route_indices,
                'route_labels': route_labels,
                'total_cost': round(float(total_cost), 2),
                'leg_breakdown': leg_breakdown,
                'optimization_result': {
                    'fval': float(result.fval) if hasattr(result, 'fval') else None,
                    'variables': result.variables if hasattr(result, 'variables') else None
                },
                'problem_info': {
                    'num_cities': n,
                    'fuel_price': self.fuel_price,
                    'fuel_burn_per_km': self.fuel_burn_per_km,
                    'distance_scale': self.distance_scale
                }
            }
            
        except Exception as e:
            logger.error(f"Error in TSP solving: {str(e)}")
            raise
    
    def _validate_inputs(self, cities, ticket_price_matrix, passenger_matrix):
        """
        Validate input data
        """
        if not cities or not isinstance(cities, dict):
            raise ValueError("Cities must be a non-empty dictionary")
        
        n = len(cities)
        if n < 2:
            raise ValueError("At least 2 cities are required")
        
        # Validate coordinates
        for city, coords in cities.items():
            if not isinstance(coords, (list, tuple)) or len(coords) != 2:
                raise ValueError(f"City {city} must have exactly 2 coordinates")
            try:
                float(coords[0])
                float(coords[1])
            except (TypeError, ValueError):
                raise ValueError(f"City {city} coordinates must be numeric")
        
        # Validate matrices
        if not isinstance(ticket_price_matrix, list) or len(ticket_price_matrix) != n:
            raise ValueError(f"Ticket price matrix must be {n}x{n}")
        
        if not isinstance(passenger_matrix, list) or len(passenger_matrix) != n:
            raise ValueError(f"Passenger matrix must be {n}x{n}")
        
        for i, row in enumerate(ticket_price_matrix):
            if not isinstance(row, list) or len(row) != n:
                raise ValueError(f"Ticket price matrix row {i} must have {n} elements")
        
        for i, row in enumerate(passenger_matrix):
            if not isinstance(row, list) or len(row) != n:
                raise ValueError(f"Passenger matrix row {i} must have {n} elements")
        
        logger.info("Input validation completed successfully")
