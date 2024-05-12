import React, { useState } from 'react';
import './SignUp.css';
import axios from 'axios';
import { ENV } from '../../constants';
import { useNavigate } from 'react-router-dom';

const SignUp = () => {
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (password !== confirmPassword) {
      alert("Passwords don't match!");
      return;
    }

    const formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('password', password);

    // Proceed with further actions like API call to backend
    try {
      const baseURL = ENV.API_BASE_URL_8000; // Port 8000 is for common-services-repo
      const response = await axios.post(`${baseURL}/common-services/login-service/create-account/`, formData);

      formData.delete('password');
      const baseURL_customer = ENV.API_BASE_URL_9000;
      const response_customer = await axios.post(`${baseURL_customer}/customer-services/create-customer/`, formData)
      console.log(response_customer.status + ": " + "'" + response_customer.data.message + "'");
      alert("Successfully signed up! You may now log in.");
    } catch (error) {
      console.error('Error signing up:', error);
      alert("Error Signing Up!");
    }
  };

  return (
    <div className="signup-container">
      <form className="signup-form" onSubmit={handleSubmit}>
        <h2>Sign Up</h2>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="confirm-password">Confirm Password</label>
          <input
            type="password"
            id="confirm-password"
            name="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        <button className='signup-button'>Sign Up</button>
      </form>
    </div>
  );
};

export default SignUp;
