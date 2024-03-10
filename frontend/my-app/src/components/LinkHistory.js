import React, { useState, useEffect } from 'react';
import axios from 'axios';

const baseURL = 'http://127.0.0.1:8000';

const LinkHistory = ({ accessToken }) => {
  const [linkHistory, setLinkHistory] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLinkHistory = async () => {
      try {
        const response = await axios.get(`${baseURL}/get_link_history`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        setLinkHistory(response.data);
        setError(null);
      } catch (error) {
        setError('Error fetching link history. Please try again.');
        setLinkHistory([]);
      }
    };

    fetchLinkHistory();
  }, [accessToken]);

  return (
    <div className='flex items-center justify-center pt-5'>
      <div>
        <div className='flex items-center justify-center text-white'>
          <h2>Link History</h2>
        </div>
        <div className='flex justify-center text-white'>
          <div>
            {error && <p style={{ color: 'red' }}>{error}</p>}
              {linkHistory.length === 0 ? (
                <p>No link history available.</p>
              ) : (
                <ul>
                  {linkHistory.map((link) => (
                    <li key={link.id}>
                      Original URL: {link.original_url}, Short URL: {link.short_url}
                    </li>
                  ))}
                </ul>
              )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LinkHistory;
