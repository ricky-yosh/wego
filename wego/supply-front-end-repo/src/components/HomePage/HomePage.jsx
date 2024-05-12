import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar from '../Navbar/Navbar';
import Table from '../Table/Table';
import MetricCard from '../MetricCard/MetricCard';
import { FaCar, FaTachometerAlt } from 'react-icons/fa';
import { Pie, Bar } from 'react-chartjs-2';
import 'chart.js/auto';
import './HomePage.css';
import { ENV } from '../../constants';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { useNavigate } from 'react-router-dom';
import QueueTable from '../Table/QueueTable';

mapboxgl.accessToken = ENV.MAPBOX_API_TOKEN;

const generateColor = () => '#' + Math.floor(Math.random() * 16777215).toString(16);

const HomePage = () => {
  const [vehicleData, setVehicleData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [chartData, setChartData] = useState({ pieData: {}, barData: {} });
  const navigate = useNavigate();

  useEffect(() => {
    fetchVehicleData();
  }, []);

  useEffect(() => {
    if (vehicleData.length > 0) {
        checkForAlerts(vehicleData);
        initializeMap();
    }
}, [vehicleData]);

const refreshVehicleData = async () => {
  fetchVehicleData();
};


  const fetchVehicleData = async () => {
    setLoading(true);
    const baseURL = ENV.API_BASE_URL_9000;
    try {
      const response = await axios.get(`${baseURL}/supply-services/fleet/get-vehicle-data/`);
      if (Array.isArray(response.data.data)) {
        setVehicleData(response.data.data);
        setChartData(calculateChartData(response.data.data));
      } else {
        throw new Error('Data format error: Expected an array');
      }
    } catch (error) {
      console.error('Error fetching vehicles:', error);
    } finally {
      setLoading(false);
    }
  };

  const checkForAlerts = (vehicles) => {
    const now = Date.now();
    vehicles.forEach(vehicle => {
        const lastResponseTime = new Date(vehicle.last_response_time).getTime();
        if (now - lastResponseTime > 300000) { // 5 minutes
            toast.error(`${vehicle.vehicle_id}: No report in last 5 minutes`, {
                position: "top-right",
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
            });
        }
        if (vehicle.battery_level <= 30 && vehicle.battery_level != null) {
            toast.error(`${vehicle.vehicle_id}: Low battery`, {
                position: "top-right",
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
            });
        }
    });
};

  const calculateChartData = (vehicles) => {
    const statusCounts = vehicles.reduce((acc, vehicle) => {
      const status = vehicle.status || 'Unknown';
      acc.statusCounts[status] = (acc.statusCounts[status] || 0) + 1;
      return acc;
    }, { statusCounts: {} });

    const typeCounts = vehicles.reduce((acc, vehicle) => {
      const type = vehicle.type || 'Unknown';
      acc[type] = (acc[type] || 0) + 1;
      return acc;
    }, {});

    const typeColors = Object.keys(typeCounts).map(generateColor);

    return {
      pieData: {
        labels: Object.keys(statusCounts.statusCounts),
        datasets: [{
          data: Object.values(statusCounts.statusCounts),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
          hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
        }]
      },
      barData: {
        labels: Object.keys(typeCounts),
        datasets: [{
          label: 'Vehicle Types',
          data: Object.values(typeCounts),
          backgroundColor: typeColors,
        }]
      }
    };
  };

  const handleActionSelected = async (vehicleId, actionType) => {
    const actionUrlMap = {
      activate: `${ENV.API_BASE_URL_9000}/supply-services/fleet/activate-vehicle/`,
      deactivate: `${ENV.API_BASE_URL_9000}/supply-services/fleet/deactivate-vehicle/`,
      delete: `${ENV.API_BASE_URL_9000}/supply-services/fleet/remove-vehicle/`
    };
  
    const formData = new FormData();
    formData.append('vehicle_id', vehicleId);
  
    try {
      const response = await axios.post(actionUrlMap[actionType], formData);
      if (response.status === 200 || response.status === 201) {
        console.log(`Action ${actionType} successful for vehicle ID: ${vehicleId}`);
        if (actionType === 'delete') {
          const updatedVehicles = vehicleData.filter(vehicle => vehicle.vehicle_id !== vehicleId);
          setVehicleData(updatedVehicles);
          setChartData(calculateChartData(updatedVehicles));
        }
      } else {
        console.error(`Failed to ${actionType} the vehicle: ${response.statusText}`);
      }
    } catch (error) {
      console.error(`Error during the ${actionType} action: ${error.toString()}`);
      alert(`Error during the ${actionType} action: ${error.toString()}`);
    }
  };
  
  const initializeMap = () => {
    const map = new mapboxgl.Map({
      container: 'mini-map',
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [-97.7431, 30.2672],
      zoom: 10,
      interactive: true
    });

    map.on('click', () => navigate('/map'));

    vehicleData.forEach(vehicle => {
      new mapboxgl.Marker()
        .setLngLat([vehicle.current_longitude, vehicle.current_latitude])
        .addTo(map);
    });
  };

  return (
    <div className="home-container">
      <ToastContainer position="top-right" autoClose={5000} hideProgressBar={false} newestOnTop={false} closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      <Navbar />
      <div className="dashboard-main">
        <div className="metrics-row">
          <MetricCard title="Total Vehicles" value={loading ? "Loading..." : vehicleData.length.toString()} icon={<FaCar size={48} />} />
          <MetricCard title="Trips Completed" value={vehicleData.filter(v => v.status === "COMPLETE").length.toString()} icon={<FaTachometerAlt size={48} />} />
          <div id="mini-map" className="mini-map" style={{ cursor: 'pointer' }}></div>
        </div>
        <Table data={vehicleData} onActionSelected={handleActionSelected} onRefresh={refreshVehicleData} />
        <div className="map-and-chart-row">
          <div className="chart-container">
            {vehicleData.length > 0 && <Bar data={chartData.barData} />}
          </div>
          <div className="chart-container">
            {vehicleData.length > 0 && <Pie data={chartData.pieData} />}
          </div>
        <QueueTable />
        </div>
      </div>
      <div className="footer">
        <div className="footer-content">© 2024 WeGo Fleet Manager Dashboard</div>
      </div>
    </div>
  );
};

export default HomePage;