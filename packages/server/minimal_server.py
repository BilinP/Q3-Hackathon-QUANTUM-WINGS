#!/usr/bin/env python3
"""
Minimal TSP Server - No external dependencies except built-in libraries
"""

import json
import math
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TSPHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        """Set CORS headers for cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        """Handle preflight OPTIONS requests"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            
            response = {
                'status': 'healthy',
                'message': 'Minimal TSP Solver API is running',
                'mode': 'minimal'
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            
            response = {'error': 'Endpoint not found'}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/solve-tsp':
            try:
                # Read request body
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                # Validate input
                if not data or 'cities' not in data:
                    raise ValueError('Missing cities data')
                
                # Solve TSP
                result = solve_tsp_minimal(data)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self._set_cors_headers()
                self.end_headers()
                
                response = {
                    'success': True,
                    'result': result,
                    'mode': 'minimal',
                    'note': 'Using minimal greedy algorithm'
                }
                self.wfile.write(json.dumps(response).encode())
                
                logger.info(f"Solved TSP for {len(data['cities'])} cities")
                
            except Exception as e:
                logger.error(f"Error solving TSP: {str(e)}")
                
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self._set_cors_headers()
                self.end_headers()
                
                response = {'error': str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            
            response = {'error': 'Endpoint not found'}
            self.wfile.write(json.dumps(response).encode())

def calculate_distance(city1_coords, city2_coords):
    """Calculate Euclidean distance between two cities"""
    x1, y1 = city1_coords
    x2, y2 = city2_coords
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def solve_tsp_minimal(data):
    """
    Minimal TSP solver using greedy nearest neighbor algorithm
    """
    cities = data['cities']
    ticket_price_matrix = data.get('ticket_price_matrix', [])
    passenger_matrix = data.get('passenger_matrix', [])
    
    # Get city names and coordinates
    city_names = list(cities.keys())
    n = len(city_names)
    
    if n < 2:
        raise ValueError("At least 2 cities required")
    
    # Create distance matrix
    distances = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            else:
                dist = calculate_distance(cities[city_names[i]], cities[city_names[j]])
                row.append(dist * 500)  # Scale to approximate km
        distances.append(row)
    
    # Create cost matrices
    fuel_price = 0.9
    fuel_burn_per_km = 2.5
    
    fuel_costs = []
    ticket_revenues = []
    edge_costs = []
    
    for i in range(n):
        fuel_row = []
        revenue_row = []
        cost_row = []
        
        for j in range(n):
            # Fuel cost
            fuel_cost = fuel_price * fuel_burn_per_km * distances[i][j]
            fuel_row.append(fuel_cost)
            
            # Ticket revenue
            if i < len(ticket_price_matrix) and j < len(ticket_price_matrix[i]) and \
               i < len(passenger_matrix) and j < len(passenger_matrix[i]):
                revenue = ticket_price_matrix[i][j] * passenger_matrix[i][j]
            else:
                revenue = 0
            revenue_row.append(revenue)
            
            # Net cost (negative means profit)
            net_cost = fuel_cost - revenue
            cost_row.append(net_cost)
        
        fuel_costs.append(fuel_row)
        ticket_revenues.append(revenue_row)
        edge_costs.append(cost_row)
    
    # Solve using greedy nearest neighbor
    route = greedy_tsp(edge_costs)
    
    # Create route labels
    route_labels = [city_names[i] for i in route] + [city_names[route[0]]]
    
    # Calculate total cost
    total_cost = 0
    for i in range(len(route)):
        from_city = route[i]
        to_city = route[(i + 1) % len(route)]
        total_cost += edge_costs[from_city][to_city]
    
    # Create leg breakdown
    leg_breakdown = []
    for i in range(len(route)):
        from_idx = route[i]
        to_idx = route[(i + 1) % len(route)]
        
        leg_breakdown.append({
            'from': city_names[from_idx],
            'to': city_names[to_idx],
            'fuel_cost': round(fuel_costs[from_idx][to_idx], 2),
            'ticket_revenue': round(ticket_revenues[from_idx][to_idx], 2),
            'net_cost': round(edge_costs[from_idx][to_idx], 2)
        })
    
    return {
        'route_indices': route,
        'route_labels': route_labels,
        'total_cost': round(total_cost, 2),
        'leg_breakdown': leg_breakdown,
        'optimization_result': {
            'fval': total_cost,
            'variables': None
        },
        'problem_info': {
            'num_cities': n,
            'fuel_price': fuel_price,
            'fuel_burn_per_km': fuel_burn_per_km,
            'distance_scale': 500,
            'algorithm': 'Greedy Nearest Neighbor'
        }
    }

def greedy_tsp(cost_matrix):
    """
    Greedy nearest neighbor TSP algorithm
    """
    n = len(cost_matrix)
    if n <= 1:
        return list(range(n))
    
    # Start from city 0
    unvisited = set(range(1, n))
    current = 0
    route = [current]
    
    while unvisited:
        # Find nearest unvisited city
        nearest = min(unvisited, key=lambda x: cost_matrix[current][x])
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    
    return route

def run_server(port=5000):
    """Run the minimal TSP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, TSPHandler)
    
    print(f"🚀 Minimal TSP Server starting on port {port}")
    print(f"🌐 Server URL: http://localhost:{port}")
    print(f"💡 Health check: http://localhost:{port}/health")
    print(f"📝 Mode: Minimal (no external dependencies)")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
