import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LanguageProvider } from './context/LanguageContext';
import Dashboard from './components/Dashboard';
import ConsentForm from './components/ConsentForm';
import VoiceAssessment from './components/VoiceAssessment';
import Profile from './components/Profile';
import Admin from './components/Admin';
import Login from './components/Login';
import Navigation from './components/Navigation';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const savedUser = localStorage.getItem('gramscore_user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('gramscore_user');
    localStorage.removeItem('gramscore_user_id');
    localStorage.removeItem('gramscore_auth_token');
    setUser(null);
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '100vh',
        flexDirection: 'column',
        gap: '1rem'
      }}>
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  // If not logged in, show login page
  if (!user) {
    return (
      <LanguageProvider>
        <Router>
          <Login onLogin={handleLogin} />
        </Router>
      </LanguageProvider>
    );
  }

  // If admin, show admin portal
  if (user.type === 'admin') {
    return (
      <LanguageProvider>
        <Router>
          <div className="app-container">
            <Navigation user={user} onLogout={handleLogout} />
            <main className="main-content">
              <Routes>
                <Route path="/admin" element={<Admin onLogout={handleLogout} />} />
                <Route path="*" element={<Navigate to="/admin" replace />} />
              </Routes>
            </main>
          </div>
        </Router>
      </LanguageProvider>
    );
  }

  // If farmer, show farmer dashboard
  return (
    <LanguageProvider>
      <Router>
        <div className="app-container">
          <Navigation user={user} onLogout={handleLogout} />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard user={user} />} />
              <Route path="/consent" element={<ConsentForm />} />
              <Route path="/assessment" element={<VoiceAssessment />} />
              <Route path="/profile" element={<Profile user={user} />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </Router>
    </LanguageProvider>
  );
}

export default App;
