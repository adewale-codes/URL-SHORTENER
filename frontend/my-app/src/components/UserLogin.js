import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const UserLogin = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    identifier: '',
    password: '',
  });

  const navigate = useNavigate();

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/user/login', formData);

      if (response.status === 200) {
        console.log('Login Successful!');
        onLogin(response.data.access_token);
        // Navigate to the home page or any desired page
        navigate('/home');
      } else {
        console.error('Login Failed. Response Status:', response.status);

        response.data.detail.forEach((detailItem, index) => {
          console.error(`Detail ${index + 1}:`, detailItem);
        });
      }
    } catch (error) {
      console.error('Error Details:', error.response ? error.response.data.detail : error.message);
    }
  };

  return (
    <div className='pt-10'>
      <div className='flex items-center justify-center'>
        <h2 className='text-xl md:text-2xl text-white font-medium'>Login</h2>
      </div>
      <div className='flex items-center pt-5 justify-center'>
        <div>
          <form>
            <div>
              <div>
                <input type="text" placeholder='Email or Username' name="identifier" onChange={handleInputChange} className='bg-white rounded px-5 py-2' />
              </div>
              <div className='pt-2'>
                <input type="password" placeholder='Password' name="password" onChange={handleInputChange} className='bg-white rounded px-5 py-2' />
              </div>
              <div className='pt-2 flex justify-center'>
                <button type="button" onClick={handleLogin} className='bg-sky-600 py-2 px-5 rounded text-white'>
                  Login
                </button>
              </div>
              <div className='text-white'>
                <p>
                  Don't have an account? <Link to="/signup">Sign up here</Link>.
                </p>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default UserLogin;
