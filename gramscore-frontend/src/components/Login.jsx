import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Lock, Users } from 'lucide-react';
import './Login.css';

const Login = ({ onLogin }) => {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({ userId: '', password: '' });
  const [loginType, setLoginType] = useState('farmer'); // 'farmer' or 'admin'
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Demo credentials
  const DEMO_FARMERS = [
    { userId: 'rajesh_kumar_001', password: 'rajesh123', name: 'Rajesh Kumar', phone: '+91-9876543210' },
    { userId: 'sunita_devi_002', password: 'sunita123', name: 'Sunita Devi', phone: '+91-9876543211' },
    { userId: 'ramesh_patil_003', password: 'ramesh123', name: 'Ramesh Patil', phone: '+91-9876543212' },
    { userId: 'lakshmi_reddy_004', password: 'lakshmi123', name: 'Lakshmi Reddy', phone: '+91-9876543213' },
    { userId: 'kumar_swamy_005', password: 'kumar123', name: 'Kumar Swamy', phone: '+91-9876543214' },
  ];

  const ADMIN_CREDENTIALS = {
    userId: 'admin',
    password: 'gramscore2024'
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    setTimeout(() => {
      if (loginType === 'admin') {
        // Admin login
        if (credentials.userId === ADMIN_CREDENTIALS.userId && 
            credentials.password === ADMIN_CREDENTIALS.password) {
          const userData = {
            type: 'admin',
            userId: 'admin',
            name: 'Administrator'
          };
          localStorage.setItem('gramscore_user', JSON.stringify(userData));
          onLogin(userData);
          navigate('/admin');
        } else {
          setError('Invalid admin credentials');
        }
      } else {
        // Farmer login
        const farmer = DEMO_FARMERS.find(
          f => f.userId === credentials.userId && f.password === credentials.password
        );
        
        if (farmer) {
          const userData = {
            type: 'farmer',
            userId: farmer.userId,
            name: farmer.name,
            phone: farmer.phone
          };
          localStorage.setItem('gramscore_user', JSON.stringify(userData));
          localStorage.setItem('gramscore_user_id', farmer.userId);
          onLogin(userData);
          navigate('/');
        } else {
          setError('Invalid farmer credentials');
        }
      }
      setLoading(false);
    }, 500);
  };

  return (
    <div className="login-container">
      <div className="login-card glass-panel">
        {/* Header */}
        <div className="login-header">
          <div className="logo-large">
            <div className="logo-icon-large">G</div>
          </div>
          <h1>GramScore AI</h1>
          <p>AI-Driven Credit Identity for Rural Bharat</p>
        </div>

        {/* Login Type Selector */}
        <div className="login-type-selector">
          <button
            className={`type-btn ${loginType === 'farmer' ? 'active' : ''}`}
            onClick={() => {
              setLoginType('farmer');
              setCredentials({ userId: '', password: '' });
              setError('');
            }}
          >
            <User size={20} />
            Farmer Login
          </button>
          <button
            className={`type-btn ${loginType === 'admin' ? 'active' : ''}`}
            onClick={() => {
              setLoginType('admin');
              setCredentials({ userId: '', password: '' });
              setError('');
            }}
          >
            <Users size={20} />
            Admin Login
          </button>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label>
              {loginType === 'admin' ? 'Username' : 'User ID'}
            </label>
            <div className="input-with-icon">
              <User size={18} />
              <input
                type="text"
                value={credentials.userId}
                onChange={(e) => setCredentials({ ...credentials, userId: e.target.value })}
                placeholder={loginType === 'admin' ? 'Enter username' : 'Enter your user ID'}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Password</label>
            <div className="input-with-icon">
              <Lock size={18} />
              <input
                type="password"
                value={credentials.password}
                onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                placeholder="Enter your password"
                required
              />
            </div>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        {/* Footer */}
        <div className="login-footer">
          <p>AWS AI Bharat Hackathon 2024</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
