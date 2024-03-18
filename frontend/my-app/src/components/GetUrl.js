import React, { useState, useEffect } from 'react';
import axios from 'axios';

const baseURL = 'https://scissor-na0r.onrender.com'; 

const GetUrl = () => {
  const [shortUrl, setShortUrl] = useState('');
  const [urlData, setUrlData] = useState(null);
  const [error, setError] = useState(null);
  const [redirecting, setRedirecting] = useState(false);

  const handleGetUrl = async () => {
    try {
      const response = await axios.get(`${baseURL}/get_url/${shortUrl}`);
      setUrlData(response.data);
    } catch (error) {
      console.error('Error getting URL:', error);
      setError('Error getting URL. Please check the provided short URL.');
      setUrlData(null); 
    }
  };

  useEffect(() => {
    const performRedirect = async () => {
      if (redirecting && urlData) {
        window.location.href = urlData.original_url;
      }
    };

    performRedirect();
  }, [redirecting, urlData]);

  const handleRedirect = async () => {
    setRedirecting(true);
  };

  const handleFetchDetails = async () => {
    await handleGetUrl();
  };

  return (
    <div className='flex items-center justify-center pt-5'>
      <div>
        <div>
          <input type="text" placeholder='Get url' className='bg-white rounded px-5 py-2' value={shortUrl} onChange={(e) => setShortUrl(e.target.value)} />
        </div>
        <div className='flex gap-2 pt-2'>
          <button onClick={handleRedirect} className='bg-sky-600 py-2 px-5 rounded text-white'>Go to URL</button>
          <button onClick={handleFetchDetails} className='bg-sky-600 py-2 px-5 rounded text-white'>Get Details</button>
        </div>
        <div className='pt-2 text-white'>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          {urlData && (
            <div>
              <p>Original URL: {urlData.original_url}</p>
              <p>Short URL: {urlData.short_url}</p>
              <p>Custom Alias: {urlData.custom_alias}</p>
              <p>Click Count: {urlData.click_count}</p>
          </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default GetUrl;
