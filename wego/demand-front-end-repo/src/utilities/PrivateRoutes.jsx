import { Navigate } from 'react-router-dom'
import { useContext } from 'react'
import AuthContext from './AuthContext'

const PrivateRoutes = ({ children }) => {
    const { user } = useContext(AuthContext);

    if (!user) {
        // User not logged in, redirect to login page
        return <Navigate to="/" />;
    }
    // User is logged in, render the children
    return children;
};

export default PrivateRoutes