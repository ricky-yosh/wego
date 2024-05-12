import { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';
import { ENV } from '../constants';

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
    let [user, setUser] = useState(null);
    let [authTokens, setAuthTokens] = useState(() =>
        localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
    );

    const navigate = useNavigate();

    useEffect(() => {
        if (authTokens && authTokens.access) {
            decodeUserFromToken(authTokens.access);
        }
    }, [authTokens]);

    const decodeUserFromToken = (token) => {
        try {
            const decodedUser = jwtDecode(token);
            setUser(decodedUser);
        } catch (error) {
            console.error('Error decoding token:', error);
        }
    };

    let loginUser = async ({ username, password }) => {
        const baseURL = ENV.API_BASE_URL_8000; // Port 8000 is for common-services-repo
        const response = await fetch(`${baseURL}/common-services/login-service/token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('authTokens', JSON.stringify(data));
            setAuthTokens(data);
            decodeUserFromToken(data.access);
            navigate('/');
        } else if (response.status == 401) {
            alert("Wrong credentials");
        }
        else {
            alert('Login failed. Please check your username and password.');
        }
    };

    let logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
        navigate('/login');
    };

    let contextData = {
        user,
        authTokens,
        loginUser,
        logoutUser,
    };

    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    );
};

