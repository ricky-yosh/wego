import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import { FaUserCircle } from 'react-icons/fa';
import './Navbar.css';
import AuthContext from '../../utilities/AuthContext';

const Navigation = () => {
  // Use the AuthContext to get the user and the logout function
  const { user, logoutUser } = useContext(AuthContext);

  return (
    <header className="header">
      <nav className="navbar">
        <NavLink to="/" className="navbar-brand">
        </NavLink>
        <div className="navbar-links">
          <NavLink to="/" className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}>
            Home
          </NavLink>
          {user ? <NavLink to="/products" className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}>
            Products
          </NavLink> : ""}
          {user ? (
            <>
              <span className="navbar-greeting">Hello, {user.username}</span>
              <button onClick={logoutUser} className="navbar-logout">
                <FaUserCircle /> Logout
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}>
                Login
              </NavLink>
              <NavLink to="/signup" className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}>
                Sign Up
              </NavLink>
            </>
          )}
        </div>
      </nav>
    </header>
  );
};

export default Navigation;
