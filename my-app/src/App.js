import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import UserLogin from './components/UserLogin';
import UserSignup from './components/UserSignup';
import CreateUrlForm from './components/CreateUrlForm';
import GetUrl from './components/GetUrl';
import QRCodeDisplay from './components/QRCodeDisplay';
import LinkHistory from './components/LinkHistory';
import Home from './components/Home';
import ForgotPassword from './components/ForgotPassword';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [accessToken, setAccessToken] = useState(null);

  const handleLogin = (token) => {
    setIsLoggedIn(true);
    setAccessToken(token);
  };

  const handleSignup = (token) => {
    setIsLoggedIn(true);
    setAccessToken(token);
  };

  return (
    <Router>
      <div className=' p-auto'>
        <div>
          <div className='flex items-center justify-center'>
            <h1 className='text-2xl md:text-4xl font-bold text-white text-center'>Welcome to my URL Shortener App</h1>
          </div>
        
          <Routes>
            <Route path="/login" element={<UserLogin onLogin={handleLogin} />} />
            <Route path="/signup" element={<UserSignup onSignup={handleSignup} />} />
            <Route path="/home" element={isLoggedIn ? <Home /> : <Navigate to="/login" />} />
            <Route path="/create" element={isLoggedIn ? <CreateUrlForm accessToken={accessToken} /> :   <Navigate to="/login" />} />
            <Route path="/get" element={isLoggedIn ? <GetUrl /> : <Navigate to="/login" />} />
            <Route path="/qrcode" element={isLoggedIn ? <QRCodeDisplay /> : <Navigate to="/login" />} />
            <Route path="/history" element={isLoggedIn ? <LinkHistory accessToken={accessToken} /> :  <Navigate to="/login" />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
          </Routes>
          {/* <nav>
            {isLoggedIn ? (
              <div>
                <Link to="/home">Home</Link>
                <Link to="/create">Create URL</Link>
                <Link to="/get">Get URL</Link>
                <Link to="/qrcode">QR Code</Link>
                <Link to="/history">Link History</Link>
              </div>
            ) : (
              <div className='flex gap-5 text-white items-center justify-center'>
              < div>
                  <button className='bg-sky-600 py-2 px-5 rounded'>
                    <Link to="/login">Login</Link>
                  </button>
                </div>
                <div>
                  <button className='bg-sky-600 py-2 px-5 rounded'>
                    <Link to="/signup">Signup</Link>
                  </button>
                </div>
              </div>
            )}
          </nav> */}
          {isLoggedIn && (
            <div>
              <CreateUrlForm accessToken={accessToken} />
              <GetUrl />
              <QRCodeDisplay />
              <LinkHistory accessToken={accessToken} />
            </div>
          )}
        </div>
      </div>
    </Router>
  );
};

export default App;
