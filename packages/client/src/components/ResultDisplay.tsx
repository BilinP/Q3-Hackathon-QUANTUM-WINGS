import React from 'react';
import type { Location } from './LocationInput';
import './ResultDisplay.css';

export interface OptimizationResult {
  route_indices: number[];
  route_labels: string[];
  total_cost: number;
  leg_breakdown: Array<{
    from: string;
    to: string;
    fuel_cost: number;
    ticket_revenue: number;
    net_cost: number;
  }>;
  optimization_result: {
    fval: number | null;
    variables: any;
  };
  problem_info: {
    num_cities: number;
    fuel_price: number;
    fuel_burn_per_km: number;
    distance_scale: number;
  };
}

interface ResultDisplayProps {
  locations: Location[];
  result: OptimizationResult;
  onBack: () => void;
  onStartOver: () => void;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ 
  locations, 
  result, 
  onBack, 
  onStartOver 
}) => {
  const isProfitable = result.total_cost < 0;
  const absoluteCost = Math.abs(result.total_cost);

  const handleExportResults = () => {
    const exportData = {
      timestamp: new Date().toISOString(),
      locations,
      optimization_result: result
    };

    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `quantum-tsp-results-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const copyResultsToClipboard = () => {
    const resultsText = `
Quantum TSP Optimization Results
================================

Optimal Route: ${result.route_labels.join(' → ')}
Total ${isProfitable ? 'Profit' : 'Cost'}: $${absoluteCost.toLocaleString()}

Route Breakdown:
${result.leg_breakdown.map(leg => 
  `${leg.from} → ${leg.to}: Fuel $${leg.fuel_cost.toLocaleString()}, Tickets $${leg.ticket_revenue.toLocaleString()}, Net $${leg.net_cost.toLocaleString()}`
).join('\n')}

Problem Parameters:
- Cities: ${result.problem_info.num_cities}
- Fuel Price: $${result.problem_info.fuel_price}/kg
- Fuel Burn Rate: ${result.problem_info.fuel_burn_per_km} kg/km
- Distance Scale: ${result.problem_info.distance_scale}x
`;

    navigator.clipboard.writeText(resultsText.trim()).then(() => {
      alert('Results copied to clipboard!');
    });
  };

  return (
    <div className="result-display-container">
      <div className="result-header">
        <button onClick={onBack} className="back-button">
          ← Back to Routes
        </button>
        <h1>Quantum Optimization Results</h1>
        <div className="header-actions">
          <button onClick={handleExportResults} className="export-button">
            📄 Export JSON
          </button>
          <button onClick={copyResultsToClipboard} className="copy-button">
            📋 Copy Results
          </button>
        </div>
      </div>

      {/* Optimization Summary */}
      <div className="result-summary">
        <div className="summary-card">
          <div className="summary-icon">
            {isProfitable ? '💰' : '💸'}
          </div>
          <div className="summary-content">
            <h2>Total {isProfitable ? 'Profit' : 'Cost'}</h2>
            <div className={`total-amount ${isProfitable ? 'profit' : 'cost'}`}>
              ${absoluteCost.toLocaleString()}
            </div>
            <p className="summary-description">
              {isProfitable 
                ? 'This route generates a net profit!' 
                : 'This route has a net cost to operate.'
              }
            </p>
          </div>
        </div>

        <div className="route-overview">
          <h3>Optimal Route</h3>
          <div className="route-path">
            {result.route_labels.map((city, index) => (
              <React.Fragment key={index}>
                <span className="route-city">{city}</span>
                {index < result.route_labels.length - 1 && (
                  <span className="route-arrow">→</span>
                )}
              </React.Fragment>
            ))}
          </div>
          <div className="route-stats">
            <div className="stat">
              <span className="stat-label">Cities Visited:</span>
              <span className="stat-value">{result.problem_info.num_cities}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Total Legs:</span>
              <span className="stat-value">{result.leg_breakdown.length}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Breakdown */}
      <div className="result-details">
        <h3>Route Leg Breakdown</h3>
        <div className="legs-container">
          {result.leg_breakdown.map((leg, index) => (
            <div key={index} className="leg-card">
              <div className="leg-header">
                <span className="leg-route">{leg.from} → {leg.to}</span>
                <span className={`leg-net ${leg.net_cost < 0 ? 'profit' : 'loss'}`}>
                  {leg.net_cost < 0 ? '+' : '-'}${Math.abs(leg.net_cost).toLocaleString()}
                </span>
              </div>
              <div className="leg-details">
                <div className="leg-item">
                  <span className="leg-label">Fuel Cost:</span>
                  <span className="leg-value cost">${leg.fuel_cost.toLocaleString()}</span>
                </div>
                <div className="leg-item">
                  <span className="leg-label">Ticket Revenue:</span>
                  <span className="leg-value revenue">${leg.ticket_revenue.toLocaleString()}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Problem Information */}
      <div className="problem-info">
        <h3>Optimization Parameters</h3>
        <div className="info-grid">
          <div className="info-item">
            <span className="info-label">Algorithm:</span>
            <span className="info-value">Quantum QAOA</span>
          </div>
          <div className="info-item">
            <span className="info-label">Fuel Price:</span>
            <span className="info-value">${result.problem_info.fuel_price}/kg</span>
          </div>
          <div className="info-item">
            <span className="info-label">Fuel Burn Rate:</span>
            <span className="info-value">{result.problem_info.fuel_burn_per_km} kg/km</span>
          </div>
          <div className="info-item">
            <span className="info-label">Distance Scale:</span>
            <span className="info-value">{result.problem_info.distance_scale}x</span>
          </div>
          {result.optimization_result.fval !== null && (
            <div className="info-item">
              <span className="info-label">Optimization Value:</span>
              <span className="info-value">{result.optimization_result.fval.toFixed(4)}</span>
            </div>
          )}
        </div>
      </div>

      {/* City Coordinates */}
      <div className="cities-info">
        <h3>City Coordinates</h3>
        <div className="cities-grid">
          {locations.map((location) => (
            <div key={location.id} className="city-card">
              <strong className="city-name">{location.name}</strong>
              <span className="city-coords">({location.x}, {location.y})</span>
            </div>
          ))}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="result-actions">
        <button onClick={onStartOver} className="start-over-button">
          🔄 Start New Optimization
        </button>
        <button onClick={onBack} className="modify-button">
          ✏️ Modify Routes
        </button>
      </div>
    </div>
  );
};

export default ResultDisplay;
