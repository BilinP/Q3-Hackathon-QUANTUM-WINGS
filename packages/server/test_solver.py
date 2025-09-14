#!/usr/bin/env python3
"""
Test script for the Quantum TSP Solver
"""

import json
import numpy as np
from quantum_tsp_solver import QuantumTSPSolver

def test_quantum_tsp_solver():
    """Test the quantum TSP solver with sample data"""
    
    # Sample data (same as in your example)
    cities = {
        "SFO": [0.0, 0.0],
        "SEA": [1.0, 3.0],
        "DEN": [4.0, 2.5],
        "DFW": [6.0, 0.5],
    }

    ticket_price_matrix = [
        [0,   200, 180, 220],   # From SFO
        [200, 0,   160, 190],   # From SEA
        [180, 160, 0,   210],   # From DEN
        [220, 190, 210, 0]      # From DFW
    ]

    passenger_matrix = [
        [0,   90, 120, 150],   # From SFO
        [100, 0,   80,  130],  # From SEA
        [110, 95,  0,   100],  # From DEN
        [140, 120, 105, 0]     # From DFW
    ]
    
    print("Testing Quantum TSP Solver...")
    print(f"Cities: {list(cities.keys())}")
    print(f"Number of cities: {len(cities)}")
    
    # Initialize solver
    solver = QuantumTSPSolver()
    
    try:
        # Solve the problem
        result = solver.solve(cities, ticket_price_matrix, passenger_matrix)
        
        # Print results
        print("\n" + "="*50)
        print("QUANTUM TSP OPTIMIZATION RESULTS")
        print("="*50)
        
        print(f"Best route: {' -> '.join(result['route_labels'])}")
        print(f"Total net cost: ${result['total_cost']:,.2f}")
        
        print("\nLeg breakdown:")
        print("-" * 60)
        for leg in result['leg_breakdown']:
            print(f"{leg['from']} -> {leg['to']}: "
                  f"fuel ${leg['fuel_cost']:,.0f}, "
                  f"tickets ${leg['ticket_revenue']:,.0f}, "
                  f"net ${leg['net_cost']:,.0f}")
        
        print("\nProblem info:")
        print(f"- Number of cities: {result['problem_info']['num_cities']}")
        print(f"- Fuel price: ${result['problem_info']['fuel_price']}/kg")
        print(f"- Fuel burn rate: {result['problem_info']['fuel_burn_per_km']} kg/km")
        
        if result['optimization_result']['fval'] is not None:
            print(f"- Optimization function value: {result['optimization_result']['fval']:.4f}")
        
        print("\nTest completed successfully! ✅")
        
        return result
        
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        raise

def test_api_format():
    """Test with the exact format that will come from the frontend API"""
    
    print("\n" + "="*50)
    print("Testing API Format Compatibility")
    print("="*50)
    
    # This is the exact format the frontend will send
    api_data = {
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
    
    print("API Data Format:")
    print(json.dumps(api_data, indent=2))
    
    solver = QuantumTSPSolver()
    result = solver.solve(
        api_data["cities"],
        api_data["ticket_price_matrix"],
        api_data["passenger_matrix"]
    )
    
    print(f"\nAPI format test successful! Route: {' -> '.join(result['route_labels'])}")
    return result

if __name__ == "__main__":
    print("🚀 Starting Quantum TSP Solver Tests")
    
    # Test 1: Basic functionality
    result1 = test_quantum_tsp_solver()
    
    # Test 2: API format compatibility
    result2 = test_api_format()
    
    print("\n🎉 All tests passed successfully!")
    print("The backend is ready to receive requests from the frontend.")
