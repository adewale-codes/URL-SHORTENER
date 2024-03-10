import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const baseURL = 'http://127.0.0.1:8000';

const UserSignup = ({ onSignup }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(null);
  const [signupSuccess, setSignupSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      if (password !== confirmPassword) {
        setError('Passwords do not match. Please check again.');
        return;
      }

      const response = await axios.post(`${baseURL}/user/register/`, {
        username,
        email,
        password,
      });

      const { token } = response.data;

      onSignup(token);

      navigate('/login');
    } catch (error) {
      console.error('Error during signup:', error);
      setError('Error during signup. Please try again.');
    }
  };

  return (
    <div className='pt-10'>
      <div className='flex items-center justify-center'>
        <h2 className='text-xl md:text-2xl font-medium text-white'>Sign Up</h2>
      </div>
      <div className='pt-5 flex items-center justify-center'>
        <div>
          <div>
            <input
              type="text"
              placeholder='Username'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className='bg-white rounded px-5 py-2 text-white'
            />
          </div>
          <div className='pt-2'>
            <input
              type="email"
              placeholder='Email'
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className='bg-white rounded px-5 py-2 text-white'
            />  
          </div>
          <div className='pt-2'>
            <input
              type="password"
              placeholder='Password'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className='bg-white rounded px-5 py-2 text-white'
            />
          </div>
          <div className='pt-2'>
            <input
              type="password"
              placeholder='Confirm password'
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className='bg-white rounded px-5 py-2 text-white'
            />
          </div>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <div className='pt-2 flex justify-center'>
            <button type="button" onClick={handleSignup} className='bg-sky-600 py-2 px-5 rounded text-white'>Sign Up</button>
          </div>
          <div className='text-white'>
            <p>
              Already have an account? <Link to="/login">Log in here</Link>.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserSignup;
