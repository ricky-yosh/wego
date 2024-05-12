import React from 'react';
import './Table.css';

const ActionDropdown = ({ vehicleId, onActionSelected }) => {
  const handleSelectChange = (e) => {
    const { value } = e.target;
    onActionSelected(vehicleId, value);
  };

  return (
    <select onChange={handleSelectChange} defaultValue="">
      <option value="" disabled>Choose Action</option>
      <option value="activate">Activate</option>
      <option value="deactivate">Deactivate</option>
      <option value="delete">Delete</option>
    </select>
  );
};

const getBatteryLevelColor = (batteryLevel) => {
  if (batteryLevel > 59) {
    return 'green';
  } else if (batteryLevel > 29) {
    return 'yellow';
  } else {
    return 'red';
  }
};

const Table = ({ data, onActionSelected, onRefresh }) => { 
  if (!data || data.length === 0) {
    return <div className="table-container">No data available.</div>;
  }

  const handleRefresh = () => {
    if (onRefresh) { 
      onRefresh();
    } else {
      console.error("Refresh function not provided.");
    }
  };


  return (
    <div className="table-container">
      <button onClick={handleRefresh} className="refresh-button">Refresh Data</button>
      <table className="table-main">
        <thead>
          <tr>
            <th>Vehicle ID</th>
            <th>Vehicle Type</th>
            <th>Last Check-in</th>
            <th>Status</th>
            <th>isActive</th>  
            <th>Trip ID</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Battery Level</th>
            <th>Actions</th>
            <th>Needs Recharging?</th>
          </tr>
        </thead>
        <tbody>
          {data.map((vehicle, index) => (
            <tr key={vehicle.vehicle_id}>
              <td>{vehicle.vehicle_id}</td>
              <td>{vehicle.type}</td>
              <td>{vehicle.last_response_time}</td>
              <td>{vehicle.status}</td>
              <td>{vehicle.is_active}</td>
              <td>{vehicle.trip_id}</td>
              <td>{vehicle.current_latitude}</td>
              <td>{vehicle.current_longitude}</td>
              <td style={{ color: getBatteryLevelColor(vehicle.battery_level) }}>
                {vehicle.battery_level !== null && vehicle.battery_level !== undefined ? `${vehicle.battery_level}%` : ''}
              </td>
              <td>
                <ActionDropdown vehicleId={vehicle.vehicle_id} onActionSelected={onActionSelected} />
              </td>
              <td>{vehicle.battery_level <= 30 ? 'Yes' : 'No'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
