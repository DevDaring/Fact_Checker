import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Navbar: React.FC = () => {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleNavigateHome = () => {
    if (isAdmin) {
      navigate('/admin');
    } else {
      navigate('/dashboard');
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand" onClick={handleNavigateHome}>
          <h2>Fact Checker</h2>
          <p className="tagline">Let's Make Difference Between Fact and Fiction</p>
        </div>
        <div className="navbar-menu">
          {user && (
            <>
              <div className="user-info">
                <span className="user-email">{user.email}</span>
                <span className="user-role-badge">{user.role}</span>
              </div>
              {!isAdmin && (
                <button onClick={() => navigate('/history')} className="btn-nav">
                  History
                </button>
              )}
              <button onClick={handleLogout} className="btn-logout">
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
