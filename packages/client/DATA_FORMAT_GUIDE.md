# Data Format Guide

This document explains how the frontend processes and formats data for the backend.

## Input Data Flow

1. **User Input**: Users enter city locations and route information through the UI
2. **Data Processing**: Frontend processes the input data
3. **Format Conversion**: Data is converted to the required backend format
4. **Console Output**: Formatted data is logged to the browser console

## Output Formats

### Cities Format
```javascript
cities = {
    "SFO": (0.0, 0.0),
    "SEA": (1.0, 3.0),
    "DEN": (4.0, 2.5),
    "DFW": (6.0, 0.5),
}
```

### Ticket Price Matrix Format
```javascript
ticket_price_matrix = np.array([
    [0,   200, 180, 220],   // From SFO
    [200, 0,   160, 190],   // From SEA
    [180, 160, 0,   210],   // From DEN
    [220, 190, 210, 0]      // From DFW
])
```

### Passenger Matrix Format
```javascript
passenger_matrix = np.array([
    [0,   90, 120, 150],   // From SFO
    [100, 0,   80,  130],  // From SEA
    [110, 95,  0,   100],  // From DEN
    [140, 120, 105, 0]     // From DFW
])
```

## How to Use

1. **Add Cities**: Enter city names and their X, Y coordinates on the first page
2. **Configure Routes**: On the second page, enter ticket prices and passenger counts for each route
3. **Submit Data**: Click the "Run" button to format and log the data to console
4. **Check Console**: Open browser developer tools to see the formatted output

## Data Processing Logic

- **Cities**: Converted to a dictionary with city names as keys and coordinate tuples as values
- **Matrices**: Created as 2D arrays where rows represent origin cities and columns represent destination cities
- **Indexing**: Cities are indexed in the order they were entered on the first page
- **Zero Values**: Diagonal elements (same city to same city) are set to 0
- **Missing Data**: Routes without price/passenger data are set to 0

## Console Output Example

When you click "Run", you'll see:
```
=== FORMATTED DATA FOR BACKEND ===
cities = {
    "SFO": (0, 0),
    "SEA": (1, 3),
    "DEN": (4, 2.5),
    "DFW": (6, 0.5),
}

ticket_price_matrix = np.array([
    [  0, 200, 180, 220],   # From SFO
    [200,   0, 160, 190],   # From SEA
    [180, 160,   0, 210],   # From DEN
    [220, 190, 210,   0]    # From DFW
])

passenger_matrix = np.array([
    [  0,  90, 120, 150],   # From SFO
    [100,   0,  80, 130],   # From SEA
    [110,  95,   0, 100],   # From DEN
    [140, 120, 105,   0]    # From DFW
])

=== RAW DATA OBJECTS ===
Cities: {SFO: [0, 0], SEA: [1, 3], DEN: [4, 2.5], DFW: [6, 0.5]}
Ticket Price Matrix: [[0, 200, 180, 220], [200, 0, 160, 190], ...]
Passenger Matrix: [[0, 90, 120, 150], [100, 0, 80, 130], ...]
```

## Files Modified

- `src/utils/dataFormatter.ts`: Core data formatting logic
- `src/utils/testDataFormatter.ts`: Test data and validation
- `src/App.tsx`: Integration with UI and console output
