import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage/HomePage';
import Navbar from './components/Navbar/Navbar';
import FleetForm from './components/Fleet/FleetForm';
import Login from './components/common-services-fm/Login/Login';
import SignUp from './components/common-services-fm/SignUp/SignUp';
import { AuthProvider } from './utilities/AuthContext';
import Map from './components/Map/Map';

function App() {
  // State to hold vehicle data
  const [vehicleData, setVehicleData] = useState([]);

  // Function to add a new vehicle
  const addVehicle = (newVehicle) => {
    setVehicleData([...vehicleData, newVehicle]);
  };

  return (
    <Router>
      <AuthProvider>
        <Navbar />
        <div className="App">
          <main className="main-content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/dashboard" element={<HomePage />} />
              <Route path="/fleet" element={<FleetForm addVehicle={addVehicle} vehicles={vehicleData} />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<SignUp />} />
              <Route path="/map" element={<Map />} />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
