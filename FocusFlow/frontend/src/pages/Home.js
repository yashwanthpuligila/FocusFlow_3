import { Link, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

function Home() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    const storedUser = localStorage.getItem('user');
    const authStatus = localStorage.getItem('isAuthenticated');
    
    if (storedUser && authStatus === 'true') {
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('isAuthenticated');
    setUser(null);
    setIsAuthenticated(false);
    alert('Logged out successfully!');
  };

  return (
    <div className="container home-container">
      {/* User Info / Auth Buttons */}
      <div style={{ 
        position: 'absolute', 
        top: '20px', 
        right: '20px',
        display: 'flex',
        gap: '10px',
        alignItems: 'center'
      }}>
        {isAuthenticated && user ? (
          <>
            <span style={{ 
              color: '#333', 
              fontWeight: '500',
              padding: '8px 16px',
              background: '#f0f2f5',
              borderRadius: '20px'
            }}>
              👤 {user.username}
            </span>
            <button 
              onClick={handleLogout}
              style={{
                padding: '8px 16px',
                background: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: '500'
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link 
              to="/login" 
              style={{
                padding: '8px 16px',
                background: '#5a6b7c',
                color: 'white',
                textDecoration: 'none',
                borderRadius: '6px',
                fontSize: '14px',
                fontWeight: '500'
              }}
            >
              Login
            </Link>
            <Link 
              to="/signup" 
              style={{
                padding: '8px 16px',
                background: '#667eea',
                color: 'white',
                textDecoration: 'none',
                borderRadius: '6px',
                fontSize: '14px',
                fontWeight: '500'
              }}
            >
              Sign Up
            </Link>
          </>
        )}
      </div>

      <h1>Welcome to FocusFlow</h1>
      {isAuthenticated && user && (
        <p style={{ fontSize: '18px', color: '#667eea', fontWeight: '500' }}>
          Hello, {user.fullName || user.username}! 👋
        </p>
      )}
      <p>Your ultimate productivity companion.</p>

      <div className="buttons">
        <Link to="/focus" className="btn"> Start Focus Session</Link>
        <Link to="/analytics" className="btn"> View Analytics</Link>
      </div>

      <div className="features">
        <div className="feature">
          <h3>Block Distractions</h3>
          <p>Stay focused by blocking distracting websites and apps automatically.</p>
          <Link to="/block" className="btn">Open Blocker</Link>
        </div>
        <div className="feature">
          <h3>Timer & Progress</h3>
          <p>Track your focus sessions with a clean timer and visual progress bar.</p>
        </div>
        <div className="feature">
          <h3> Insights</h3>
          <p>Visualize your productivity stats over time and optimize your focus strategy.</p>
        </div>
      </div>
    </div>
  );
}

export default Home;
