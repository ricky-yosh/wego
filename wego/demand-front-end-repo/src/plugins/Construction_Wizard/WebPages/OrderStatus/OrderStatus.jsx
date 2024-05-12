import { useParams } from 'react-router-dom';
import './OrderStatus.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { ENV } from '../../../../constants';

function OrderStatus({ NavigationComponent }) {
    const { project_name, order_id } = useParams();
    // const [orderStatusInfo, setOrderStatusInfo] = useState({ "status": '' });
    const [tripInfo, setTripInfo] = useState({
        "trip_id": null,
        "status": "PENDING",
        "vehicle_id": null,
        "vehicle_type": null,
        "initial_destination": "",
        "final_destination": "",
        "route": null,
        "pickup_waypoint": null,
        "dropoff_waypoint": null,
        "order_id": null,
        "time_created": "",
        "trip_percentage": null
    });
    useEffect(() => {
        fetchOrderAndTripStatus();
    }, [order_id]);

    async function fetchOrderAndTripStatus() {
        const baseUrl = ENV.API_BASE_URL_9000;
        const tripStatusEndpoint = `${baseUrl}/demand-services/construction-wizard/get-trip-status/`;

        try {
            const tripResponsePromise = axios.post(tripStatusEndpoint, { "order_id": order_id });
            const [tripResponse] = await Promise.all([tripResponsePromise]);

            if (tripResponse.status === 200) {
                const tripData = tripResponse.data['data']['trip'];
                const updatedTripInfo = {};

                // Iterate over keys to update status if empty or copy the value
                Object.keys(tripData).forEach(key => {
                    const value = tripData[key];
                    if (key === "status" && value === "") {
                        updatedTripInfo[key] = "PENDING"; // Set to PENDING if status is empty
                    } else {
                        updatedTripInfo[key] = value; // Otherwise, use the existing value
                    }
                });

                // Update the state once with all modifications
                setTripInfo(prevTripState => ({
                    ...prevTripState,
                    ...updatedTripInfo
                }));
            } else {
                setTripInfo(prevTripState => ({
                    ...prevTripState,
                    "final_destination": "Not available",
                    "status": "PENDING"
                }));
            }
        } catch (error) {
            console.error("Fetching trip data failed:", error);
            setTripInfo(prevTripState => ({
                ...prevTripState,
                "status": "ERROR FETCHING TRIP DATA",
                "final_destination": "Not available"
            }));
        }
    }

    return (
        <>
            <NavigationComponent projectName={project_name} pageType={"OrderStatus"} />
            <div className="order-status-container">
                <h1>Order Status for {project_name} - Order: {order_id} - {tripInfo.status}</h1>
                <div className="status-details">
                    <div className="destination">
                        Destination: {tripInfo.final_destination}
                    </div>
                    <div className="completion">
                        Order Completion: {tripInfo.trip_percentage !== null ? `${tripInfo.trip_percentage.toFixed(2)}%` : 'Calculating...'}
                        <div className="progress-bar-container">
                            <div className="progress-bar" style={{ width: `${tripInfo.trip_percentage}%` }}></div>
                        </div>
                    </div>
                </div>
                <div className="map-container">
                    {/* Placeholder for map component */}
                    Map goes here
                </div>
            </div>
        </>
    );
}

export default OrderStatus;
