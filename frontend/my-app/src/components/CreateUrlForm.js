import React, { useState } from 'react';
import axios from 'axios';

const baseURL = 'https://scissor-na0r.onrender.com';

const CreateUrlForm = () => {
  const [originalUrl, setOriginalUrl] = useState('');
  const [customAlias, setCustomAlias] = useState('');
  const [error, setError] = useState(null);
  const [shortenedUrl, setShortenedUrl] = useState(null);

  const handleCreateUrl = async () => {
    try {
      const token = localStorage.getItem('access_token');

      const response = await axios.post(
        `${baseURL}/create_url/`,
        {
          original_url: originalUrl,
          custom_alias: customAlias,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json', // Add this line to set the content type
          },
        }
      );

      if (response.status === 200) {
        const { shortened_url } = response.data;
        setShortenedUrl(shortened_url);
        setError(null);
      } else {
        console.error('Error creating short URL. Response Status:', response.status);
        setError('An unexpected error occurred. Please try again later.');
      }
    } catch (error) {
      console.error('Error creating short URL:', error.response ? error.response.data.detail : error.message);
      if (error.response) {
        if (error.response.status === 400) {
          setError(error.response.data.detail);
        } else if (error.response.status === 401) {
          setError('Unauthorized. Please log in.');
        } else if (error.response.status === 422 && error.response.data.detail === 'Alias already exists') {
          setError('Alias already exists. Please choose a different one.');
        } else {
          setError('An unexpected error occurred. Please try again later.');
        }
      } else {
        setError('An unexpected error occurred. Please try again later.');
      }
    }
  };

  const handleCustomAliasChange = () => {
    setError(null);
  };

  return (
    <div className='flex items-centier justify-center'>
      <div>
        <div>
          <input type="text" placeholder='Create url' className='bg-white rounded px-5 py-2' value= {originalUrl} onChange={(e) => setOriginalUrl(e.target.value)} />
        </div>
        <div className='pt-2'>
          <input
            type="text"
            placeholder='Custom alias'
            className='bg-white rounded px-5 py-2'
            value={customAlias}
            onChange={(e) => {
              setCustomAlias(e.target.value);
              handleCustomAliasChange();
            }}
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {shortenedUrl && <p className='text-white'>Your shortened URL: {shortenedUrl}</p>}
        <div className='pt-2 flex justify-center'>
          <button onClick={handleCreateUrl} className='bg-sky-600 py-2 px-5 rounded text-white'>Create Short URL</button>
        </div>
      </div>
    </div>
  );
};

export default CreateUrlForm;
