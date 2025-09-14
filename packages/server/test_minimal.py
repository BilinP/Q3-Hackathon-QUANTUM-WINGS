#!/usr/bin/env python3
"""
Test script for the minimal server
"""

import json
import urllib.request
import urllib.parse

def test_minimal_server():
    """Test the minimal server functionality"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Minimal TSP Server...")
    
    # Test 1: Health check
    try:
        print("\n1. Testing health endpoint...")
        response = urllib.request.urlopen(f"{base_url}/health")
        data = json.loads(response.read().decode())
        print(f"   ✅ Health check: {data['status']} ({data['mode']})")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False
    
    # Test 2: TSP solving
    try:
        print("\n2. Testing TSP solving...")
        
        test_data = {
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
        
        # Prepare request
        data = json.dumps(test_data).encode()
        req = urllib.request.Request(
            f"{base_url}/solve-tsp",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Send request
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        
        if result['success']:
            print(f"   ✅ TSP solved successfully!")
            print(f"   📍 Route: {' → '.join(result['result']['route_labels'])}")
            print(f"   💰 Total cost: ${result['result']['total_cost']:,.2f}")
            print(f"   🔧 Algorithm: {result['result']['problem_info']['algorithm']}")
        else:
            print(f"   ❌ TSP solving failed")
            return False
            
    except Exception as e:
        print(f"   ❌ TSP test failed: {e}")
        return False
    
    print("\n🎉 All tests passed!")
    print("The minimal server is working correctly.")
    return True

if __name__ == '__main__':
    print("Make sure the server is running first:")
    print("python minimal_server.py")
    print()
    input("Press Enter when server is ready...")
    test_minimal_server()
