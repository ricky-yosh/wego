import { useState, useEffect } from 'react';
import React, { useContext } from 'react';
import axios from 'axios';
import './CreateProject.css'
import AuthContext from '/src/utilities/AuthContext.jsx';
import { ENV } from '/src/constants'

function CreateProject({ NavigationComponent }) {
    // Access user from the AuthContext
    const { user } = useContext(AuthContext);

    const initialProjectState = {
        "username": user.username,  // Use conditional access
        "project_name": "",
        "description": "",
        "start_date": "",
        "end_date": "",
        "status": "In Progress",
        "priority": "Low"
    };

    const [Project, updateProject] = useState(initialProjectState)

    const handleInput = event => {
        const key = event.target.name
        const value = event.target.value

        // Update the state based on the key and value
        updateProject(prevState => ({
            ...prevState, // Spread the previous state helps manage multiple elements in Project dict without overiding the previous state
            [key]: value // Update the value for the specified key
        }));

    }

    const create_project = async event => {
        event.preventDefault();
        const baseURL_customer = ENV.API_BASE_URL_9000;
        const api = `${baseURL_customer}/demand-services/construction-wizard/create_project/`;
        try {
            const response = await axios.post(api, Project);
            if (response.status === 200) {
                console.log(response);
                alert("SUCCESSFULLY CREATED PROJECT");
                updateProject(initialProjectState);
            }
        } catch (error) {
            alert("ERROR CREATING PROJECT");
        }
    }

    return (
        <>
            <NavigationComponent /> {/* Directly render the NavigationComponent */}
            <div className='Project-Form-Container'>
                <h1>
                    Create New Project
                </h1>
                <div className='Form-Data-Container'>
                    <form onSubmit={create_project}>
                        <label>Project Name</label><br /><br />
                        <input name='project_name' value={Project.project_name} onChange={handleInput} type='text' placeholder='Enter Project Name' required /><br /><br />

                        <label>Project Description</label><br /><br />
                        <textarea name='description' value={Project.description} onChange={handleInput} className='Form-Project-Description' placeholder='Enter Project Description' required /><br /><br />

                        <label>Start Date</label><br /><br />
                        <input name='start_date' value={Project.start_date} onChange={handleInput} type='date' placeholder='Select Project Start Date' required /><br /><br />

                        <label>End Date</label><br /><br />
                        <input name='end_date' value={Project.end_date} onChange={handleInput} type='date' placeholder='Select Project End Date' required /><br /><br />

                        <label>Priority</label><br /><br />
                        <select name='priority' onChange={handleInput} type='text' placeholder='Select Project Priority' required>
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                        </select><br /><br /><br /><br />
                        <div className="submit-container">
                            <input type="submit" value="Create Project" />
                        </div>
                    </form>
                </div>
            </div>
        </>
    )
}
export default CreateProject;