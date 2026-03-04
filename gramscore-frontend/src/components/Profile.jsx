import React, { useState, useEffect } from 'react';
import { User, MapPin, Phone, Calendar, TrendingUp, Award, Target, Lightbulb, CheckCircle, AlertCircle } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../services/api';
import './Profile.css';

const Profile = ({ user }) => {
  const { t } = useLanguage();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [aiInsights, setAiInsights] = useState(null);

  useEffect(() => {
    loadUserProfile();
  }, [user]);

  const loadUserProfile = async () => {
    try {
      // Get user ID from prop or localStorage
      const userId = user?.userId || api.getCurrentUserId() || 'rajesh_kumar_001';

      // Mock user data (in production, fetch from API)
      const mockUserData = {
        user_id: 'rajesh_kumar_001',
        name: 'Rajesh Kumar',
        phone: '+91-9876543210',
        location: 'Pune, Maharashtra',
        coordinates: { lat: 18.5204, lon: 73.8567 },
        profile: {
          age: 42,
          experience_years: 20,
          land_acres: 3.5,
          crops: ['Rice', 'Wheat', 'Vegetables'],
          education: 'High School',
          family_size: 5,
          farming_type: 'Mixed Farming'
        },
        gramscore: 785,
        risk_level: 'Low',
        score_history: [
          { date: '2024-03-01', score: 785 },
          { date: '2024-02-01', score: 770 },
          { date: '2024-01-01', score: 755 },
          { date: '2023-12-01', score: 740 },
        ],
        achievements: [
          { id: 1, title: 'Digital Pioneer', description: 'Used UPI for 90+ consecutive days', icon: '📱', earned: true },
          { id: 2, title: 'Consistent Farmer', description: 'Maintained NDVI above 0.7 for 6 months', icon: '🌾', earned: true },
          { id: 3, title: 'Bill Master', description: 'Paid all utility bills on time for 12 months', icon: '⚡', earned: true },
          { id: 4, title: 'Credit Champion', description: 'Score above 750', icon: '🏆', earned: true },
          { id: 5, title: 'Future Planner', description: 'Completed financial planning assessment', icon: '🎯', earned: false },
        ],
        strengths: [
          'Excellent UPI transaction consistency (92%)',
          'Strong agricultural productivity (NDVI: 0.72)',
          'Reliable utility payment history',
          'High financial discipline',
          'Good digital literacy'
        ],
        improvements: [
          'Consider diversifying crop portfolio',
          'Explore crop insurance options',
          'Build emergency fund to 6 months expenses',
          'Learn about government subsidy schemes'
        ],
        ai_insights: {
          summary: 'Rajesh Kumar demonstrates excellent creditworthiness with consistent financial behavior and strong agricultural productivity. His digital payment adoption and reliable bill payment history indicate high financial discipline.',
          recommendations: [
            {
              title: 'Expand Agricultural Operations',
              description: 'With your excellent credit score, you qualify for equipment financing at 9% interest. Consider investing in modern irrigation systems to improve yield.',
              priority: 'high',
              potential_impact: 'Increase income by 25-30%'
            },
            {
              title: 'Crop Insurance',
              description: 'Enroll in Pradhan Mantri Fasal Bima Yojana (PMFBY) to protect against crop loss. Premium is subsidized by government.',
              priority: 'medium',
              potential_impact: 'Risk mitigation'
            },
            {
              title: 'Financial Literacy Program',
              description: 'Join our advanced financial planning workshop to learn about investment options and tax benefits for farmers.',
              priority: 'low',
              potential_impact: 'Better financial planning'
            }
          ],
          next_steps: [
            'Apply for equipment loan (Pre-approved: ₹2,00,000)',
            'Complete crop insurance enrollment',
            'Set up automatic bill payments',
            'Attend financial literacy workshop'
          ]
        }
      };

      setUserData(mockUserData);
      setAiInsights(mockUserData.ai_insights);
      setLoading(false);
    } catch (error) {
      console.error('Error loading profile:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container animate-fade-in text-center" style={{ paddingTop: '3rem' }}>
        <div className="loading-spinner"></div>
        <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>Loading profile...</p>
      </div>
    );
  }

  if (!userData) {
    return (
      <div className="container animate-fade-in text-center" style={{ paddingTop: '3rem' }}>
        <p style={{ color: 'var(--text-muted)' }}>Unable to load profile</p>
      </div>
    );
  }

  const scoreChange = userData.score_history.length >= 2
    ? userData.score_history[0].score - userData.score_history[1].score
    : 0;

  return (
    <div className="profile-container container animate-fade-in">
      {/* Header Section */}
      <div className="profile-header glass-panel">
        <div className="profile-avatar">
          <User size={48} />
        </div>
        <div className="profile-info">
          <h1>{userData.name}</h1>
          <div className="profile-meta">
            <span><MapPin size={16} /> {userData.location}</span>
            <span><Phone size={16} /> {userData.phone}</span>
            <span><Calendar size={16} /> {userData.profile.experience_years} years farming</span>
          </div>
        </div>
        <div className="profile-score">
          <div className="score-badge">
            <div className="score-value">{userData.gramscore}</div>
            <div className="score-label">GramScore</div>
          </div>
          {scoreChange !== 0 && (
            <div className={`score-change ${scoreChange > 0 ? 'positive' : 'negative'}`}>
              <TrendingUp size={16} />
              {scoreChange > 0 ? '+' : ''}{scoreChange} this month
            </div>
          )}
        </div>
      </div>

      {/* Farm Details */}
      <div className="profile-section glass-panel">
        <h2>🌾 Farm Details</h2>
        <div className="farm-details-grid">
          <div className="detail-item">
            <div className="detail-label">Land Size</div>
            <div className="detail-value">{userData.profile.land_acres} acres</div>
          </div>
          <div className="detail-item">
            <div className="detail-label">Crops</div>
            <div className="detail-value">{userData.profile.crops.join(', ')}</div>
          </div>
          <div className="detail-item">
            <div className="detail-label">Farming Type</div>
            <div className="detail-value">{userData.profile.farming_type}</div>
          </div>
          <div className="detail-item">
            <div className="detail-label">Family Size</div>
            <div className="detail-value">{userData.profile.family_size} members</div>
          </div>
        </div>
      </div>

      {/* AI Insights Section */}
      {aiInsights && (
        <div className="profile-section glass-panel ai-insights-section">
          <h2><Lightbulb size={24} /> AI-Powered Insights</h2>
          <div className="ai-summary">
            {aiInsights.summary}
          </div>

          <h3 style={{ marginTop: '2rem', marginBottom: '1rem' }}>Personalized Recommendations</h3>
          <div className="recommendations-grid">
            {aiInsights.recommendations.map((rec, index) => (
              <div key={index} className={`recommendation-card priority-${rec.priority}`}>
                <div className="rec-header">
                  <h4>{rec.title}</h4>
                  <span className={`priority-badge ${rec.priority}`}>
                    {rec.priority === 'high' ? '🔥' : rec.priority === 'medium' ? '⭐' : '💡'}
                    {rec.priority.toUpperCase()}
                  </span>
                </div>
                <p>{rec.description}</p>
                <div className="rec-impact">
                  <Target size={16} />
                  <span>{rec.potential_impact}</span>
                </div>
              </div>
            ))}
          </div>

          <h3 style={{ marginTop: '2rem', marginBottom: '1rem' }}>Next Steps</h3>
          <div className="next-steps-list">
            {aiInsights.next_steps.map((step, index) => (
              <div key={index} className="next-step-item">
                <CheckCircle size={20} />
                <span>{step}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Strengths & Improvements */}
      <div className="profile-section-row">
        <div className="glass-panel strengths-panel">
          <h2><Award size={24} /> Your Strengths</h2>
          <ul className="strengths-list">
            {userData.strengths.map((strength, index) => (
              <li key={index}>
                <CheckCircle size={18} />
                <span>{strength}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="glass-panel improvements-panel">
          <h2><AlertCircle size={24} /> Areas to Improve</h2>
          <ul className="improvements-list">
            {userData.improvements.map((improvement, index) => (
              <li key={index}>
                <TrendingUp size={18} />
                <span>{improvement}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Achievements */}
      <div className="profile-section glass-panel">
        <h2>🏆 Achievements</h2>
        <div className="achievements-grid">
          {userData.achievements.map((achievement) => (
            <div key={achievement.id} className={`achievement-card ${achievement.earned ? 'earned' : 'locked'}`}>
              <div className="achievement-icon">{achievement.icon}</div>
              <div className="achievement-info">
                <h4>{achievement.title}</h4>
                <p>{achievement.description}</p>
              </div>
              {achievement.earned && (
                <div className="achievement-badge">
                  <CheckCircle size={20} />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Score History */}
      <div className="profile-section glass-panel">
        <h2>📈 Score History</h2>
        <div className="score-history-chart">
          {userData.score_history.map((entry, index) => (
            <div key={index} className="score-history-item">
              <div className="score-bar" style={{ height: `${(entry.score / 900) * 100}%` }}>
                <span className="score-value">{entry.score}</span>
              </div>
              <div className="score-date">{new Date(entry.date).toLocaleDateString('en-US', { month: 'short' })}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Profile;
