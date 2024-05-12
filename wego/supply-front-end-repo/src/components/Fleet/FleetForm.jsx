import React, { useState } from 'react';
import axios from 'axios';
import './FleetForm.css';
import { ENV } from '../../constants';

const FleetForm = ({ addVehicle, vehicles }) => {
  const [vehicle_id, setVehicleId] = useState('');
  const [type, setVehicleType] = useState('');

  const formatVehicleId = (id) => {
    //UPPERCASE-#### (e.g., ABCD-1234)
    return id.toUpperCase();
  };

  const isValidVehicleId = (id) => {
    // Regular expression to check the format: Four letters, a dash, followed by four digits
    const regex = /^[A-Z]{4}-\d{4}$/;
    return regex.test(id);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!vehicle_id || !type) {
      alert('Please fill in all fields');
      return;
    }

    const formattedVehicleId = formatVehicleId(vehicle_id);

    if (!isValidVehicleId(formattedVehicleId)) {
      alert('Vehicle ID must be in the format XXXX-#### (e.g., TEST-1234)');
      return;
    }

    const formData = new FormData();
    formData.append('vehicle_id', formattedVehicleId);
    formData.append('type', type);

    try {
      const baseURL = ENV.API_BASE_URL_9000;
      const response = await axios.post(`${baseURL}/supply-services/fleet/add-vehicle/`, formData);
      
      if (response.status === 200 || response.status === 201) {
        alert('Vehicle added successfully!');
        addVehicle(formattedVehicleId, type); // Update local state with formatted ID
        console.log(formattedVehicleId, type);
        // Clear form fields after successful submission
        setVehicleId('');
        setVehicleType('');
      } else {
        alert('Failed to add vehicle. Please try again!');
      }
    } catch (error) {
      console.error('Error adding vehicle:', error);
      alert('Error adding vehicle. Please check the console for more information.');
    }
  };

  return (
    <div className="fleet-form-container">
      <div className="fleet-form-section">
        <h2 className="fleet-form-heading">Add New Vehicle</h2>
        <form onSubmit={handleSubmit} className="fleet-form">
          <label className="fleet-form-label">Vehicle ID</label>
          <input
            className="fleet-form-input"
            type="text"
            value={vehicle_id}
            onChange={(e) => setVehicleId(e.target.value)}
            placeholder="Format: XXXX-####"
            required
          />
          <label className="fleet-form-label">Vehicle Type</label>
          <select
            className="fleet-form-input"
            value={type}
            onChange={(e) => setVehicleType(e.target.value)}
            required
          >
            <option value="">Select a vehicle type</option>
            <option value="Truck">Truck</option>
            <option value="Car">Car</option>
            <option value="Drone">Drone</option>
          </select>
          <button className="fleet-form-button" type="submit">Add Vehicle</button>
        </form>
      </div>
    </div>
  );
};

export default FleetForm;
