import axios from 'axios';
import { useParams } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import { ENV } from '../../../../constants';

function Orders({ NavigationComponent, GenericBodyComponent }) {

    const { project_name } = useParams(); // Destructuring to get params
    const [orders, setOrders] = useState([]);
    useEffect(() => {
        fetchProjectOrders();
    }, []);

    async function fetchProjectOrders() {

        const baseUrl = ENV.API_BASE_URL_9000;
        const apiEndpoint = `${baseUrl}/demand-services/construction-wizard/get-project-orders/`
        const project_data = {
            "project_name": project_name
        }
        const response = await axios.post(apiEndpoint, project_data)
        if (response.status === 200) {
            setOrders(response.data["orders"])
        }
    }

    return (
        <>
            <NavigationComponent projectName={project_name} pageType={"Orders"} />
            <GenericBodyComponent title="Current Orders" items={orders} itemType="Order" imageSrc={'/cart.jpg'} urlParam={project_name} />
        </>
    )
}

export default Orders