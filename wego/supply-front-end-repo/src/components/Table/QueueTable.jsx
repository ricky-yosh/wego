import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ENV } from '../../constants';
import './Table.css';

const QueueTable = () => {
    const [queueData, setQueueData] = useState([]);
    const [loading, setLoading] = useState(true);

    // Fetch data from the server
    const fetchQueueData = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${ENV.API_BASE_URL_9000}/supply-services/dispatcher/get-unassigned-trips/`);
            setQueueData(response.data.filter(trip => trip.vehicle_id === null));  // filter trips still waiting for assignment
            setLoading(false);
        } catch (error) {
            console.error('Error fetching queue data:', error);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchQueueData();
    }, []);

    const handleRefresh = () => {
        fetchQueueData();
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="table-container small-table-container">
            <button onClick={handleRefresh} className="refresh-button">Refresh Trip Data</button>
            <table className="table-main">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Pickup Address</th>
                        <th>Dropoff Address</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {queueData.map(trip => (
                        <tr key={trip.trip_id}>
                            <td>{trip.order_id}</td>
                            <td>{trip.initial_destination}</td>
                            <td>{trip.final_destination}</td>
                            <td>{trip.vehicle_id ? 'Assigned' : 'Waiting for assignment'}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default QueueTable;
