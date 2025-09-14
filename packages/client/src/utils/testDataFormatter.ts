import type { Location } from '../components/LocationInput';
import type { Route } from '../components/RouteConfiguration';
import { formatDataForBackend, formatDataForConsole } from './dataFormatter';

// Test data similar to your example
const testLocations: Location[] = [
  { id: '1', name: 'SFO', x: 0.0, y: 0.0 },
  { id: '2', name: 'SEA', x: 1.0, y: 3.0 },
  { id: '3', name: 'DEN', x: 4.0, y: 2.5 },
  { id: '4', name: 'DFW', x: 6.0, y: 0.5 }
];

const testRoutes: Route[] = [
  // From SFO
  { id: '1', from: 'SFO', to: 'SEA', distance: 3.16, ticketPrice: 200, numberOfPassengers: 90 },
  { id: '2', from: 'SFO', to: 'DEN', distance: 4.47, ticketPrice: 180, numberOfPassengers: 120 },
  { id: '3', from: 'SFO', to: 'DFW', distance: 6.02, ticketPrice: 220, numberOfPassengers: 150 },
  
  // From SEA
  { id: '4', from: 'SEA', to: 'SFO', distance: 3.16, ticketPrice: 200, numberOfPassengers: 100 },
  { id: '5', from: 'SEA', to: 'DEN', distance: 3.04, ticketPrice: 160, numberOfPassengers: 80 },
  { id: '6', from: 'SEA', to: 'DFW', distance: 5.59, ticketPrice: 190, numberOfPassengers: 130 },
  
  // From DEN
  { id: '7', from: 'DEN', to: 'SFO', distance: 4.47, ticketPrice: 180, numberOfPassengers: 110 },
  { id: '8', from: 'DEN', to: 'SEA', distance: 3.04, ticketPrice: 160, numberOfPassengers: 95 },
  { id: '9', from: 'DEN', to: 'DFW', distance: 2.5, ticketPrice: 210, numberOfPassengers: 100 },
  
  // From DFW
  { id: '10', from: 'DFW', to: 'SFO', distance: 6.02, ticketPrice: 220, numberOfPassengers: 140 },
  { id: '11', from: 'DFW', to: 'SEA', distance: 5.59, ticketPrice: 190, numberOfPassengers: 120 },
  { id: '12', from: 'DFW', to: 'DEN', distance: 2.5, ticketPrice: 210, numberOfPassengers: 105 }
];

export function runDataFormatterTest(): void {
  console.log('=== TESTING DATA FORMATTER ===');
  
  const formattedData = formatDataForBackend(testLocations, testRoutes);
  const consoleOutput = formatDataForConsole(formattedData);
  
  console.log('Test Input Locations:', testLocations);
  console.log('Test Input Routes:', testRoutes);
  console.log('\n' + consoleOutput);
  
  console.log('=== TEST COMPLETE ===');
}
