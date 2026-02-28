import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LanguageProvider } from './context/LanguageContext';
import Dashboard from './components/Dashboard';
import ConsentForm from './components/ConsentForm';
import VoiceAssessment from './components/VoiceAssessment';
import Navigation from './components/Navigation';

function App() {
  return (
    <LanguageProvider>
      <Router>
        <div className="app-container">
          <Navigation />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/consent" element={<ConsentForm />} />
              <Route path="/assessment" element={<VoiceAssessment />} />
              <Route path="/profile" element={
                <div className="container animate-fade-in text-center" style={{ paddingTop: '3rem' }}>
                  <h2>Profile</h2>
                  <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>Coming soon</p>
                </div>
              } />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </Router>
    </LanguageProvider>
  );
}

export default App;
