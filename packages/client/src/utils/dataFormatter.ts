import type { Location } from '../components/LocationInput';
import type { Route } from '../components/RouteConfiguration';

export interface FormattedData {
  cities: Record<string, [number, number]>;
  ticket_price_matrix: number[][];
  passenger_matrix: number[][];
}

export function formatDataForBackend(locations: Location[], routes: Route[]): FormattedData {
  // Create cities object with coordinates
  const cities: Record<string, [number, number]> = {};
  locations.forEach(location => {
    cities[location.name] = [location.x, location.y];
  });

  // Create city name to index mapping
  const cityNames = locations.map(loc => loc.name);
  const cityIndexMap: Record<string, number> = {};
  cityNames.forEach((name, index) => {
    cityIndexMap[name] = index;
  });

  // Initialize matrices with zeros
  const numCities = locations.length;
  const ticketPriceMatrix: number[][] = Array(numCities).fill(null).map(() => Array(numCities).fill(0));
  const passengerMatrix: number[][] = Array(numCities).fill(null).map(() => Array(numCities).fill(0));

  // Fill matrices with route data
  routes.forEach(route => {
    const fromIndex = cityIndexMap[route.from];
    const toIndex = cityIndexMap[route.to];
    
    if (fromIndex !== undefined && toIndex !== undefined) {
      // Only fill if we have valid data
      if (route.ticketPrice > 0) {
        ticketPriceMatrix[fromIndex][toIndex] = route.ticketPrice;
      }
      if (route.numberOfPassengers > 0) {
        passengerMatrix[fromIndex][toIndex] = route.numberOfPassengers;
      }
    }
  });

  return {
    cities,
    ticket_price_matrix: ticketPriceMatrix,
    passenger_matrix: passengerMatrix
  };
}

export function formatDataForConsole(formattedData: FormattedData): string {
  let output = '';
  
  // Format cities
  output += 'cities = {\n';
  Object.entries(formattedData.cities).forEach(([cityName, coords]) => {
    output += `    "${cityName}": (${coords[0]}, ${coords[1]}),\n`;
  });
  output += '}\n\n';
  
  // Format ticket price matrix
  output += 'ticket_price_matrix = np.array([\n';
  formattedData.ticket_price_matrix.forEach((row, index) => {
    const cityName = Object.keys(formattedData.cities)[index];
    const formattedRow = row.map(price => price.toString().padStart(3, ' ')).join(', ');
    output += `    [${formattedRow}],   # From ${cityName}\n`;
  });
  output += '])\n\n';
  
  // Format passenger matrix
  output += 'passenger_matrix = np.array([\n';
  formattedData.passenger_matrix.forEach((row, index) => {
    const cityName = Object.keys(formattedData.cities)[index];
    const formattedRow = row.map(passengers => passengers.toString().padStart(3, ' ')).join(', ');
    output += `    [${formattedRow}],   # From ${cityName}\n`;
  });
  output += '])\n';
  
  return output;
}
