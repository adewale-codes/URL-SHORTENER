import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const baseURL = 'https://scissor-na0r.onrender.com';

const ResetPassword = () => {
  const [newPassword, setNewPassword] = useState('');
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const { token } = useParams();

  const handleResetPassword = async () => {
    try {
      const response = await axios.post(`${baseURL}/user/reset-password`, {
        token,
        new_password: newPassword,
      });

      setSuccessMessage(response.data.message);
      setError(null);
    } catch (error) {
      setError('Invalid or expired token.');
      setSuccessMessage(null);
    }
  };

  return (
    <div>
      <h2>Reset Password</h2>
      <label>
        New Password:
        <input
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
      </label>
      <br />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
      <button onClick={handleResetPassword}>Submit</button>
    </div>
  );
};

export default ResetPassword;
