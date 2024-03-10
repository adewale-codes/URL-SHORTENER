import React, { useState } from 'react';
import axios from 'axios';

const baseURL = 'http://127.0.0.1:8000';

const ForgotPassword = () => {
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const handleForgotPassword = async () => {
    try {
      const response = await axios.post(`${baseURL}/user/forgot-password`, {
        username_or_email: usernameOrEmail,
      });

      setSuccessMessage(response.data.message);
      setError(null);
    } catch (error) {
      setError('User not found or an error occurred.');
      setSuccessMessage(null);
    }
  };

  return (
    <div>
      <h2>Forgot Password</h2>
      <label>
        Username or Email:
        <input
          type="text"
          value={usernameOrEmail}
          onChange={(e) => setUsernameOrEmail(e.target.value)}
        />
      </label>
      <br />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
      <button onClick={handleForgotPassword}>Reset Password</button>
    </div>
  );
};

export default ForgotPassword;
