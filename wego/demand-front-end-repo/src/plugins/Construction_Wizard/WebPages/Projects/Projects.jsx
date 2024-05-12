import React, { useState, useEffect, useContext } from 'react';
import { ENV } from '../../../../constants';
import axios from 'axios';
import AuthContext from '../../../../utilities/AuthContext';

function Projects({ NavigationComponent, GenericBodyComponent }) {

    const { user } = useContext(AuthContext);
    const [projectItems, setProjectItems] = useState([]);

    // Fetch projects whenever the user data changes and is not null
    useEffect(() => {
        fetchData();
    }, [user]);  // Add `user` as a dependency to ensure fetchData is called when user is updated

    async function fetchData() {
        const baseUrl = ENV.API_BASE_URL_9000;
        const endpoint = `${baseUrl}/demand-services/construction-wizard/get-projects/`;
        const data = { "username": user.username };

        const response = await axios.post(endpoint, data);
        if (response.status === 200) {
            setProjectItems(response.data.projects); // Assuming 'projects' is the correct key
        }
    }

    return (
        <>
            <NavigationComponent />
            <GenericBodyComponent title='Your Projects' items={projectItems} itemType='Project' imageSrc={'/2012-apple-folder-emoji.png'} />
        </>
    );
}

export default Projects;
