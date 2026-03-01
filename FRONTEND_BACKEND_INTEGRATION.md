# 🔗 GramScore Frontend-Backend Integration Guide

## 📋 Overview

This document explains how the **GramScore AI backend** (Python/Streamlit prototype) integrates with the **existing React frontend** (gramscore-frontend).

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    GramScore System                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │  React Frontend  │ ◄─────► │  Backend API     │         │
│  │  (Port 5173)     │  REST   │  (Python/Flask)  │         │
│  │                  │  API    │                  │         │
│  │  - Dashboard     │         │  - Score Engine  │         │
│  │  - Consent Form  │         │  - ML Models     │         │
│  │  - Voice Assess  │         │  - AWS Services  │         │
│  └──────────────────┘         └──────────────────┘         │
│           │                            │                     │
│           │                            │                     │
│           ▼                            ▼                     │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │  Streamlit Demo  │         │  Data Sources    │         │
│  │  (Port 8501)     │         │  - Account Agg   │         │
│  │                  │         │  - Satellite     │         │
│  │  Standalone      │         │  - Weather       │         │
│  │  Prototype       │         │  - Utilities     │         │
│  └──────────────────┘         └──────────────────┘         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Two Integration Approaches

### Approach 1: Standalone Streamlit (Current Implementation)
**Status**: ✅ Fully Functional

The Streamlit app (`gramscore_prototype/app.py`) is a **standalone prototype** that:
- Runs independently on port 8501
- Contains its own UI and backend logic
- Perfect for demos and hackathon presentations
- No integration needed with React frontend

**Use Case**: Quick demos, testing, hackathon presentations

### Approach 2: REST API Backend (Production Ready)
**Status**: 🔧 Architecture Ready, Implementation Needed

Create a Flask/FastAPI backend that serves the React frontend:
- Backend exposes REST APIs
- React frontend consumes APIs
- Proper separation of concerns
- Production-grade architecture

**Use Case**: Production deployment, scalable applications

---

## 🚀 Current Integration Status

### What's Already Built

#### 1. **Streamlit Prototype** (`gramscore_prototype/`)
```python
# Standalone application with:
- User interface (Streamlit)
- Backend logic (Python)
- AWS integration (Mock/Real)
- ML models (XGBoost, Random Forest)
- Data sources (Account Aggregator, Satellite, etc.)
```

#### 2. **React Frontend** (`gramscore-frontend/`)
```javascript
// React application with:
- Dashboard component
- Consent form
- Voice assessment
- Multi-language support
- Navigation
```

### Integration Points Needed

To connect the React frontend with the Python backend, you need:

1. **Backend API Server** (Flask/FastAPI)
2. **API Endpoints** for score calculation
3. **CORS Configuration** for cross-origin requests
4. **Authentication** (JWT tokens)
5. **WebSocket** for real-time updates (optional)

---

## 🔧 Implementation Guide

### Step 1: Create Flask API Backend

Create `gramscore_prototype/api_server.py`:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from ml_models import GramScoreMLModel
from aws_services import AWSServicesOrchestrator
from data_sources import DataSourceOrchestrator
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize services
ml_model = GramScoreMLModel('xgboost')
ml_model.train()  # Train model on startup
aws_services = AWSServicesOrchestrator()
data_orchestrator = DataSourceOrchestrator()

# Secret key for JWT
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Authentication middleware
def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user_id']
        except:
            return jsonify({'error': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorator

# API Endpoints

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'ml_model': ml_model.is_trained,
            'aws': aws_services.health_check()
        }
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User authentication"""
    data = request.json
    user_id = data.get('user_id')
    phone = data.get('phone')
    
    # In production, verify credentials against database
    # For demo, generate token directly
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'token': token,
        'user_id': user_id,
        'expires_in': 86400
    })

@app.route('/api/consent', methods=['POST'])
@token_required
def submit_consent(current_user):
    """Submit user consent for data access"""
    data = request.json
    
    consent_data = {
        'user_id': current_user,
        'data_types': data.get('data_types', []),
        'timestamp': datetime.now().isoformat(),
        'consent_given': True
    }
    
    # Store consent in database (mock for demo)
    return jsonify({
        'success': True,
        'consent_token': f'consent_{current_user}_{int(datetime.now().timestamp())}',
        'message': 'Consent recorded successfully'
    })

@app.route('/api/data/collect', methods=['POST'])
@token_required
def collect_user_data(current_user):
    """Collect data from all sources"""
    data = request.json
    
    user_profile = {
        'user_id': current_user,
        'location': data.get('location', {})
    }
    
    # Collect data from all sources
    collected_data = data_orchestrator.collect_all_data(user_profile)
    
    return jsonify({
        'success': True,
        'data': collected_data,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/score/calculate', methods=['POST'])
@token_required
def calculate_score(current_user):
    """Calculate GramScore"""
    data = request.json
    
    # Prepare features
    features = {
        'upi_consistency': data.get('upi_consistency', 50),
        'transaction_volume': data.get('transaction_volume', 10000),
        'ndvi_avg': data.get('ndvi_avg', 0.4),
        'utility_payment_score': data.get('utility_payment_score', 60),
        'psychometric_score': data.get('psychometric_score', 60),
        'weather_impact': data.get('weather_impact', 0.8),
        'land_size': data.get('land_size', 1.0),
        'crop_types': data.get('crop_types', [])
    }
    
    # Calculate score using ML model
    prediction = ml_model.predict(features)
    
    # Get AWS insights
    aws_result = aws_services.calculate_comprehensive_score(features)
    
    return jsonify({
        'success': True,
        'gramscore': prediction['predicted_score'],
        'confidence': prediction['confidence'],
        'components': prediction['feature_importance'],
        'ai_insights': aws_result.get('ai_insights', ''),
        'risk_level': 'Low' if prediction['predicted_score'] >= 750 else 'Medium' if prediction['predicted_score'] >= 500 else 'High',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/score/history/<user_id>', methods=['GET'])
@token_required
def get_score_history(current_user, user_id):
    """Get user's score history"""
    # In production, fetch from DynamoDB
    # For demo, return mock data
    return jsonify({
        'success': True,
        'scores': [
            {
                'score': 720,
                'date': '2024-01-15',
                'components': {
                    'transaction_frequency': 85,
                    'agricultural_productivity': 70,
                    'utility_payments': 75,
                    'psychometric_score': 80
                }
            }
        ]
    })

@app.route('/api/voice/assess', methods=['POST'])
@token_required
def voice_assessment(current_user):
    """Process voice assessment"""
    data = request.json
    
    responses = data.get('responses', {})
    language = data.get('language', 'english')
    
    # Process voice assessment
    from voice_assessment import VoiceAssessmentService
    voice_service = VoiceAssessmentService()
    analysis = voice_service.analyze_voice_responses(responses, language)
    
    return jsonify({
        'success': True,
        'psychometric_score': analysis['overall_score'],
        'category_scores': analysis['category_scores'],
        'recommendations': analysis['recommendations']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Step 2: Update React Frontend to Call APIs

Update `gramscore-frontend/src/services/api.js`:

```javascript
// API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Helper function for API calls
const apiCall = async (endpoint, options = {}) => {
  const token = localStorage.getItem('auth_token');
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : '',
      ...options.headers,
    },
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }
  
  return response.json();
};

// API functions
export const api = {
  // Authentication
  login: (credentials) => 
    apiCall('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    }),

  // Consent
  submitConsent: (consentData) =>
    apiCall('/consent', {
      method: 'POST',
      body: JSON.stringify(consentData),
    }),

  // Data Collection
  collectData: (userData) =>
    apiCall('/data/collect', {
      method: 'POST',
      body: JSON.stringify(userData),
    }),

  // Score Calculation
  calculateScore: (features) =>
    apiCall('/score/calculate', {
      method: 'POST',
      body: JSON.stringify(features),
    }),

  // Score History
  getScoreHistory: (userId) =>
    apiCall(`/score/history/${userId}`),

  // Voice Assessment
  submitVoiceAssessment: (assessmentData) =>
    apiCall('/voice/assess', {
      method: 'POST',
      body: JSON.stringify(assessmentData),
    }),

  // Health Check
  healthCheck: () =>
    apiCall('/health'),
};
```

### Step 3: Update Dashboard Component

Update `gramscore-frontend/src/components/Dashboard.jsx`:

```javascript
import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import './Dashboard.css';

function Dashboard() {
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userData, setUserData] = useState({
    upi_consistency: 70,
    ndvi_avg: 0.5,
    utility_payment_score: 75,
    psychometric_score: 65,
  });

  const calculateScore = async () => {
    setLoading(true);
    try {
      const result = await api.calculateScore(userData);
      setScore(result);
    } catch (error) {
      console.error('Error calculating score:', error);
      alert('Failed to calculate score. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <h1>🌾 GramScore Dashboard</h1>
      
      {/* User Input Section */}
      <div className="input-section">
        <h2>Your Information</h2>
        <div className="input-grid">
          <div className="input-group">
            <label>UPI Transaction Consistency (%)</label>
            <input
              type="range"
              min="0"
              max="100"
              value={userData.upi_consistency}
              onChange={(e) => setUserData({
                ...userData,
                upi_consistency: parseInt(e.target.value)
              })}
            />
            <span>{userData.upi_consistency}%</span>
          </div>
          
          <div className="input-group">
            <label>Agricultural Productivity (NDVI)</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={userData.ndvi_avg}
              onChange={(e) => setUserData({
                ...userData,
                ndvi_avg: parseFloat(e.target.value)
              })}
            />
            <span>{userData.ndvi_avg.toFixed(2)}</span>
          </div>
        </div>
        
        <button 
          onClick={calculateScore}
          disabled={loading}
          className="calculate-btn"
        >
          {loading ? 'Calculating...' : '🚀 Calculate GramScore'}
        </button>
      </div>

      {/* Score Display Section */}
      {score && (
        <div className="score-section">
          <div className={`score-display ${score.risk_level.toLowerCase()}-risk`}>
            <h2>Your GramScore</h2>
            <div className="score-value">{score.gramscore}</div>
            <div className="risk-level">{score.risk_level} Risk</div>
          </div>
          
          <div className="score-breakdown">
            <h3>Score Components</h3>
            {Object.entries(score.components).map(([key, value]) => (
              <div key={key} className="component-bar">
                <span>{key.replace(/_/g, ' ')}</span>
                <div className="bar">
                  <div 
                    className="bar-fill" 
                    style={{ width: `${value * 100}%` }}
                  />
                </div>
                <span>{(value * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>

          {score.ai_insights && (
            <div className="ai-insights">
              <h3>🤖 AI Insights</h3>
              <p>{score.ai_insights}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Dashboard;
```

### Step 4: Environment Configuration

Create `gramscore-frontend/.env`:

```bash
# API Configuration
REACT_APP_API_URL=http://localhost:5000/api

# AWS Configuration (optional)
REACT_APP_AWS_REGION=ap-south-1

# Feature Flags
REACT_APP_ENABLE_VOICE_ASSESSMENT=true
REACT_APP_ENABLE_SATELLITE_DATA=true
```

---

## 🚀 Running the Integrated System

### Terminal 1: Start Backend API
```bash
cd gramscore_prototype
python api_server.py
# Backend runs on http://localhost:5000
```

### Terminal 2: Start React Frontend
```bash
cd gramscore-frontend
npm install
npm run dev
# Frontend runs on http://localhost:5173
```

### Terminal 3: Start Streamlit Demo (Optional)
```bash
cd gramscore_prototype
streamlit run app.py
# Demo runs on http://localhost:8501
```

---

## 📊 Data Flow

```
User Action (React) 
    ↓
API Request (fetch/axios)
    ↓
Flask Backend (api_server.py)
    ↓
ML Model (ml_models.py)
    ↓
AWS Services (aws_services.py)
    ↓
Data Sources (data_sources.py)
    ↓
Response (JSON)
    ↓
React State Update
    ↓
UI Render
```

---

## 🔒 Security Considerations

1. **Authentication**: JWT tokens for API access
2. **CORS**: Properly configured for production domains
3. **Rate Limiting**: Prevent API abuse
4. **Input Validation**: Sanitize all user inputs
5. **HTTPS**: Use SSL/TLS in production
6. **Environment Variables**: Never commit secrets to git

---

## 🎯 Current Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Streamlit Prototype | ✅ Complete | Standalone demo app |
| React Frontend | ✅ Complete | UI components ready |
| Flask API Backend | 🔧 Template Ready | Needs implementation |
| AWS Integration | ✅ Complete | Mock + Real modes |
| ML Models | ✅ Complete | Trained and ready |
| Data Sources | ✅ Complete | Mock data working |

---

## 🚀 Next Steps for Full Integration

1. **Implement Flask API** using the template above
2. **Add API service** to React frontend
3. **Update components** to use API calls
4. **Test end-to-end** flow
5. **Deploy** to production (AWS ECS/Fargate)

---

## 💡 Recommendation

For the **AWS AI Bharat Hackathon**, I recommend:

1. **Use Streamlit prototype** for live demos (it's complete and impressive)
2. **Show React frontend** as the production UI design
3. **Explain integration architecture** using this document
4. **Demonstrate** both UIs to show versatility

This approach showcases:
- ✅ Working prototype (Streamlit)
- ✅ Production-ready UI (React)
- ✅ Scalable architecture (Flask API)
- ✅ AWS integration (Bedrock, SageMaker)

---

**Built with ❤️ for Rural Bharat | Powered by AWS AI Services**