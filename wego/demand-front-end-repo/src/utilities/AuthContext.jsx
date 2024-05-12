import { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';
import { ENV } from '../constants';

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
    const navigate = useNavigate();

    const getInitialTokens = () => {
        const tokenString = localStorage.getItem('authTokens');
        return tokenString ? JSON.parse(tokenString) : null;
    };

    let [authTokens, setAuthTokens] = useState(getInitialTokens);
    let [user, setUser] = useState(() => {
        const tokens = getInitialTokens();
        return tokens ? jwtDecode(tokens.access) : null;
    });

    const decodeUserFromToken = (token) => {
        try {
            return jwtDecode(token);
        } catch (error) {
            console.error('Error decoding token:', error);
            return null;
        }
    };

    useEffect(() => {
        if (authTokens && authTokens.access) {
            const decodedUser = decodeUserFromToken(authTokens.access);
            setUser(decodedUser);
        } else {
            setUser(null);
        }
    }, [authTokens]);

    let loginUser = async ({ username, password }) => {
        const baseURL = ENV.API_BASE_URL_8000;
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
            navigate('/');
        } else if (response.status === 401) {
            alert("Wrong credentials");
        } else {
            alert('Login failed. Please check your username and password.');
        }
    };

    let logoutUser = () => {
        localStorage.removeItem('authTokens');
        setAuthTokens(null);
        setUser(null);
        navigate('/');
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

