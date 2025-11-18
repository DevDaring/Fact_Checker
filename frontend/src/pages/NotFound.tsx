import React from 'react';
import { useNavigate } from 'react-router-dom';

const NotFound: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="not-found-page">
      <div className="not-found-container">
        <h1>404</h1>
        <h2>Page Not Found</h2>
        <p>The page you're looking for doesn't exist.</p>
        <button className="btn-home" onClick={() => navigate('/')}>
          Go Home
        </button>
      </div>
    </div>
  );
};

export default NotFound;
