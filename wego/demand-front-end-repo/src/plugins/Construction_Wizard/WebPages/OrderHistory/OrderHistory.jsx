import axios from 'axios';
import { useParams } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import { ENV } from '../../../../constants';

function OrderHistory({ NavigationComponent }) {
    // Log to check if the NavigationComponent is correctly passed
    return (
        <>
            <NavigationComponent />
            <div>
                <h1>Order history</h1>
            </div>
        </>
    );
}


export default OrderHistory;