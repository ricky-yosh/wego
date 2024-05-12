import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import { FaTruck, FaUserCircle } from 'react-icons/fa';
import './Navbar.css';
import AuthContext from '../../utilities/AuthContext';

const Navbar = () => {
  // Use the AuthContext to get the user and the logout function
  const { user, logoutUser } = useContext(AuthContext);

  return (
    <header className="header">
      <nav className="navbar">
        <NavLink to="/" className="navbar-brand">
          <FaTruck size={28} />
          Fleet Manager
        </NavLink>
        <div className="navbar-links">
          <NavLink to="/dashboard" className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}>
            Dashboard
          </NavLink>
          <NavLink to="/fleet" className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}>
            Fleet
          </NavLink>
          <NavLink to="/map" className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}>
            Map
          </NavLink>
          {user ? (
            // If there is a user, greet them and provide a logout button
            <>
              <span className="navbar-greeting">Hi, {user.username}</span>
              <button onClick={logoutUser} className="navbar-logout">Logout</button>
            </>
          ) : (
            // If no user, provide links to login and sign up
            <>
              <NavLink to="/login" className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}>
                Login
              </NavLink>
              <NavLink to="/signup" className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}>
                Signup
              </NavLink>
            </>
          )}
        </div>
      </nav>
    </header>
  );
};

export default Navbar;