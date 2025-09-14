import React, { useState } from 'react'
import LocationInput from './components/LocationInput'
import RouteConfiguration from './components/RouteConfiguration'
import ResultDisplay from './components/ResultDisplay'
import type { Location } from './components/LocationInput'
import type { Route } from './components/RouteConfiguration'
import type { OptimizationResult } from './components/ResultDisplay'
import { formatDataForBackend, formatDataForConsole } from './utils/dataFormatter'
// import { runDataFormatterTest } from './utils/testDataFormatter'
import './App.css'

type AppPage = 'location-input' | 'route-configuration' | 'result-display';

function App() {
  const [currentPage, setCurrentPage] = useState<AppPage>('location-input');
  const [locations, setLocations] = useState<Location[]>([]);
  const [, setRoutes] = useState<Route[]>([]);
  const [optimizationResult, setOptimizationResult] = useState<OptimizationResult | null>(null);

  // Run test on component mount (for development)
  React.useEffect(() => {
    // Uncomment the line below to run the test
    // runDataFormatterTest();
  }, []);

  const handleLocationNext = (locationData: Location[]) => {
    setLocations(locationData);
    setCurrentPage('route-configuration');
  };

  const handleRouteBack = () => {
    setCurrentPage('location-input');
  };

  const handleResultBack = () => {
    setCurrentPage('route-configuration');
  };

  const handleStartOver = () => {
    setCurrentPage('location-input');
    setLocations([]);
    setRoutes([]);
    setOptimizationResult(null);
  };

  const handleRouteSubmit = async (routeData: Route[]) => {
    setRoutes(routeData);
    
    try {
      // Format data according to the specified backend format
      const formattedData = formatDataForBackend(locations, routeData);
      
      // Log formatted data for debugging
      console.log('=== FORMATTED DATA FOR BACKEND ===');
      const consoleOutput = formatDataForConsole(formattedData);
      console.log(consoleOutput);
      
      console.log('=== RAW DATA OBJECTS ===');
      console.log('Cities:', formattedData.cities);
      console.log('Ticket Price Matrix:', formattedData.ticket_price_matrix);
      console.log('Passenger Matrix:', formattedData.passenger_matrix);
      
      // Send data to backend API
      console.log('🚀 Sending data to quantum TSP solver...');
      
      const API_BASE_URL = 'http://localhost:5000';
      const response = await fetch(`${API_BASE_URL}/solve-tsp`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formattedData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
      }
      
      const result = await response.json();
      
      if (result.success) {
        console.log('✅ Quantum TSP Optimization Results:');
        console.log('Best route:', result.result.route_labels.join(' -> '));
        console.log(`Total cost: $${result.result.total_cost.toLocaleString()}`);
        console.log('Detailed breakdown:', result.result.leg_breakdown);
        
        // Store the result and navigate to result page
        setOptimizationResult(result.result);
        setCurrentPage('result-display');
      } else {
        throw new Error('Backend returned unsuccessful result');
      }
      
    } catch (error) {
      console.error('❌ Error during quantum optimization:', error);
      
      const errorMessage = error instanceof Error ? error.message : String(error);
      
      if (error instanceof TypeError && errorMessage.includes('fetch')) {
        alert(
          '🔌 Connection Error!\n\n' +
          'Cannot connect to the backend server.\n' +
          'Please make sure the Python backend is running on http://localhost:5000\n\n' +
          'To start the backend:\n' +
          '1. Open terminal in the server folder\n' +
          '2. Run: python app.py\n' +
          '3. Then try again'
        );
      } else {
        alert(
          `❌ Quantum Optimization Error!\n\n` +
          `${errorMessage}\n\n` +
          `Please check the console for more details.`
        );
      }
    }
  };

  return (
    <div className="app">
      {currentPage === 'location-input' && (
        <LocationInput onNext={handleLocationNext} />
      )}
      {currentPage === 'route-configuration' && (
        <RouteConfiguration
          locations={locations}
          onBack={handleRouteBack}
          onSubmit={handleRouteSubmit}
        />
      )}
      {currentPage === 'result-display' && optimizationResult && (
        <ResultDisplay
          locations={locations}
          result={optimizationResult}
          onBack={handleResultBack}
          onStartOver={handleStartOver}
        />
      )}
    </div>
  )
}

export default App
