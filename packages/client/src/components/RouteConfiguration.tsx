import React, { useState, useEffect } from 'react';
import type { Location } from './LocationInput';
import './RouteConfiguration.css';

export interface Route {
  id: string;
  from: string;
  to: string;
  distance: number;
  ticketPrice: number;
  numberOfPassengers: number;
}

interface RouteConfigurationProps {
  locations: Location[];
  onBack: () => void;
  onSubmit: (routes: Route[]) => void;
}

const RouteConfiguration: React.FC<RouteConfigurationProps> = ({ 
  locations, 
  onBack, 
  onSubmit 
}) => {
  const [routes, setRoutes] = useState<Route[]>([]);

  // Calculate distance between two points
  const calculateDistance = (loc1: Location, loc2: Location): number => {
    const dx = loc2.x - loc1.x;
    const dy = loc2.y - loc1.y;
    return Math.round(Math.sqrt(dx * dx + dy * dy) * 100) / 100;
  };

  // Generate all possible route combinations
  const generateAllRoutes = (locations: Location[]): Route[] => {
    const allRoutes: Route[] = [];
    let routeId = 1;

    // Generate routes between all city pairs (bidirectional)
    for (let i = 0; i < locations.length; i++) {
      for (let j = i + 1; j < locations.length; j++) {
        const loc1 = locations[i];
        const loc2 = locations[j];
        const distance = calculateDistance(loc1, loc2);

        // Add bidirectional routes
        allRoutes.push({
          id: (routeId++).toString(),
          from: loc1.name,
          to: loc2.name,
          distance,
          ticketPrice: 0,
          numberOfPassengers: 0
        });

        allRoutes.push({
          id: (routeId++).toString(),
          from: loc2.name,
          to: loc1.name,
          distance,
          ticketPrice: 0,
          numberOfPassengers: 0
        });
      }
    }

    return allRoutes;
  };

  useEffect(() => {
    const generatedRoutes = generateAllRoutes(locations);
    setRoutes(generatedRoutes);
  }, [locations]);

  const updateRoute = (routeId: string, field: 'ticketPrice' | 'numberOfPassengers', value: number) => {
    setRoutes(routes.map(route => 
      route.id === routeId ? { ...route, [field]: value } : route
    ));
  };

  const handleSubmit = () => {
    const routesWithData = routes.filter(route => 
      route.ticketPrice > 0 || route.numberOfPassengers > 0
    );

    if (routesWithData.length === 0) {
      alert('Please enter ticket price or passenger count for at least one route');
      return;
    }

    onSubmit(routes);
  };

  const getTotalRoutes = () => routes.length;
  const getConfiguredRoutes = () => routes.filter(route => 
    route.ticketPrice > 0 || route.numberOfPassengers > 0
  ).length;

  return (
    <div className="route-configuration-container">
      <div className="header">
        <button onClick={onBack} className="back-button">
          ← Back
        </button>
        <h1>Route Configuration</h1>
        <div className="route-summary">
          <span>Total Routes: {getTotalRoutes()}</span>
          <span>Configured: {getConfiguredRoutes()}</span>
        </div>
      </div>

      <div className="locations-summary">
        <h3>City List:</h3>
        <div className="locations-grid">
          {locations.map((location) => (
            <div key={location.id} className="location-card">
              <strong>{location.name}</strong>
              <span>({location.x}, {location.y})</span>
            </div>
          ))}
        </div>
      </div>

      <div className="routes-container">
        <h3>All Possible Routes:</h3>
        <div className="routes-grid">
          {routes.map((route) => (
            <div key={route.id} className="route-card">
              <div className="route-info">
                <div className="route-path">
                  <span className="from">{route.from}</span>
                  <span className="arrow">→</span>
                  <span className="to">{route.to}</span>
                </div>
                <div className="distance">
                  Distance: {route.distance} units
                </div>
              </div>
              
              <div className="route-inputs">
                <div className="input-group">
                  <label>Ticket Price:</label>
                  <input
                    type="number"
                    min="0"
                    step="0.01"
                    value={route.ticketPrice || ''}
                    onChange={(e) => updateRoute(route.id, 'ticketPrice', parseFloat(e.target.value) || 0)}
                    placeholder="0.00"
                    className="price-input"
                  />
                </div>
                
                <div className="input-group">
                  <label>Passengers:</label>
                  <input
                    type="number"
                    min="0"
                    value={route.numberOfPassengers || ''}
                    onChange={(e) => updateRoute(route.id, 'numberOfPassengers', parseInt(e.target.value) || 0)}
                    placeholder="0"
                    className="passenger-input"
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="submit-button-container">
        <button
          onClick={handleSubmit}
          className="run-button"
        >
          Run
        </button>
      </div>
    </div>
  );
};

export default RouteConfiguration;
