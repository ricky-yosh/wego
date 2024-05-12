import './Login.css';
import React, { useState, useContext } from 'react';
import AuthContext from '../../../utilities/AuthContext';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  const { loginUser } = useContext(AuthContext);

  const handleSubmit = async (event) => {
    event.preventDefault();
    loginUser({ username, password });
 };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Login</h2>
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
        <button type="submit" >Login</button>
      </form>
    </div>
  );
};

export default Login;