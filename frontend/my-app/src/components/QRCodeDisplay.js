import React, { useState } from 'react';
import axios from 'axios';
import QRCode from 'qrcode.react';

const baseURL = 'http://127.0.0.1:8000';

const QRCodeDisplay = () => {
  const [shortUrl, setShortUrl] = useState('');
  const [qrCodePath, setQRCodePath] = useState('');
  const [error, setError] = useState('');

  const handleGetQRCode = async () => {
    try {
      const response = await axios.get(`${baseURL}/get_qr_code/${shortUrl}`, {
        responseType: 'arraybuffer',
      });

      const imageData = new Uint8Array(response.data); 
      const imageUrl = `data:image/png;base64,${arrayBufferToBase64(imageData)}`;
      setQRCodePath(imageUrl);
    } catch (error) {
      console.error('Error getting QR code:', error);
      setError('Error getting QR code. Please try again.');
    }
  };

  const arrayBufferToBase64 = (buffer) => {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  };

  return (
    <div className='flex items-center justify-center pt-5'>
      <div>
        <div>
          <input type="text" placeholder='Short url' className='bg-white rounded px-5 py-2' value={shortUrl} onChange={(e) => setShortUrl(e.target.value)} />
        </div>
        <div className='pt-2 flex justify-center'>
          <button onClick={handleGetQRCode} className='bg-sky-600 py-2 px-5 rounded text-white'>Get QR Code</button>
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {qrCodePath && (
          <div className='pt-2'>
            <div className='flex justify-center'>
              <p className='text-white'>QR Code:</p>
            </div>
            <div className='flex justify-center'>
              <QRCode value={qrCodePath} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default QRCodeDisplay;
