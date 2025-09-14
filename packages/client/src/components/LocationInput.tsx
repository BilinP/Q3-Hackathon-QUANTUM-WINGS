import React, { useState } from 'react';
import './LocationInput.css';

export interface Location {
  id: string;
  name: string;
  x: number;
  y: number;
}

interface LocationInputProps {
  onNext: (locations: Location[]) => void;
}

const LocationInput: React.FC<LocationInputProps> = ({ onNext }) => {
  const [locations, setLocations] = useState<Location[]>([
    { id: '1', name: '', x: 0, y: 0 }
  ]);

  const addLocation = () => {
    const newId = (locations.length + 1).toString();
    setLocations([...locations, { id: newId, name: '', x: 0, y: 0 }]);
  };

  const removeLocation = (id: string) => {
    if (locations.length > 1) {
      setLocations(locations.filter(loc => loc.id !== id));
    }
  };

  const updateLocation = (id: string, field: keyof Location, value: string | number) => {
    setLocations(locations.map(loc => 
      loc.id === id ? { ...loc, [field]: value } : loc
    ));
  };

  const handleNext = () => {
    const validLocations = locations.filter(loc => loc.name.trim() !== '');
    if (validLocations.length >= 2) {
      onNext(validLocations);
    } else {
      alert('Please enter at least two city locations');
    }
  };

  const isFormValid = () => {
    const validLocations = locations.filter(loc => loc.name.trim() !== '');
    return validLocations.length >= 2;
  };

  return (
    <div className="location-input-container">
      <h1>City Location Input</h1>
      <div className="location-form">
        {locations.map((location, index) => (
          <div key={location.id} className="location-row">
            <div className="location-input-group">
              <label>Location {index + 1}:</label>
              <input
                type="text"
                placeholder="Enter city name"
                value={location.name}
                onChange={(e) => updateLocation(location.id, 'name', e.target.value)}
                className="location-name-input"
              />
            </div>
            <div className="coordinate-inputs">
              <div className="coordinate-input">
                <label>X:</label>
                <input
                  type="number"
                  value={location.x}
                  onChange={(e) => updateLocation(location.id, 'x', parseInt(e.target.value) || 0)}
                  className="coordinate-field"
                />
              </div>
              <div className="coordinate-input">
                <label>Y:</label>
                <input
                  type="number"
                  value={location.y}
                  onChange={(e) => updateLocation(location.id, 'y', parseInt(e.target.value) || 0)}
                  className="coordinate-field"
                />
              </div>
            </div>
            {locations.length > 1 && (
              <button
                type="button"
                onClick={() => removeLocation(location.id)}
                className="remove-button"
              >
                Remove
              </button>
            )}
          </div>
        ))}
        
        <div className="form-actions">
          <button
            type="button"
            onClick={addLocation}
            className="add-location-button"
          >
            Add City
          </button>
        </div>
      </div>

      <div className="next-button-container">
        <button
          onClick={handleNext}
          disabled={!isFormValid()}
          className="next-button"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default LocationInput;
