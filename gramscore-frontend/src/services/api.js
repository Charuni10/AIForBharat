/**
 * GramScore AI - API Service
 * Handles all backend API communications
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

/**
 * Helper function for making API calls
 */
const apiCall = async (endpoint, options = {}) => {
  const token = localStorage.getItem('gramscore_auth_token');
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
  };

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || `API Error: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Call Error:', error);
    throw error;
  }
};

/**
 * API Service Object
 */
export const api = {
  // ============================================================================
  // AUTHENTICATION
  // ============================================================================
  
  /**
   * Login user and get authentication token
   */
  login: async (credentials) => {
    const response = await apiCall('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    
    if (response.success && response.token) {
      localStorage.setItem('gramscore_auth_token', response.token);
      localStorage.setItem('gramscore_user_id', response.user_id);
    }
    
    return response;
  },

  /**
   * Logout user
   */
  logout: () => {
    localStorage.removeItem('gramscore_auth_token');
    localStorage.removeItem('gramscore_user_id');
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: () => {
    return !!localStorage.getItem('gramscore_auth_token');
  },

  /**
   * Get current user ID
   */
  getCurrentUserId: () => {
    return localStorage.getItem('gramscore_user_id');
  },

  // ============================================================================
  // HEALTH CHECK
  // ============================================================================
  
  /**
   * Check API health status
   */
  healthCheck: () => apiCall('/health'),

  // ============================================================================
  // CONSENT MANAGEMENT
  // ============================================================================
  
  /**
   * Submit user consent for data access
   */
  submitConsent: (consentData) =>
    apiCall('/consent', {
      method: 'POST',
      body: JSON.stringify(consentData),
    }),

  // ============================================================================
  // DATA COLLECTION
  // ============================================================================
  
  /**
   * Collect user data from all sources
   */
  collectData: (userData) =>
    apiCall('/data/collect', {
      method: 'POST',
      body: JSON.stringify(userData),
    }),

  // ============================================================================
  // SCORE CALCULATION
  // ============================================================================
  
  /**
   * Calculate GramScore based on user features
   */
  calculateScore: (features) =>
    apiCall('/score/calculate', {
      method: 'POST',
      body: JSON.stringify(features),
    }),

  /**
   * Get user's score history
   */
  getScoreHistory: (userId) =>
    apiCall(`/score/history/${userId}`),

  // ============================================================================
  // VOICE ASSESSMENT
  // ============================================================================
  
  /**
   * Submit voice assessment responses
   */
  submitVoiceAssessment: (assessmentData) =>
    apiCall('/voice/assess', {
      method: 'POST',
      body: JSON.stringify(assessmentData),
    }),

  // ============================================================================
  // TRANSACTION ANALYSIS
  // ============================================================================
  
  /**
   * Analyze transaction patterns
   */
  analyzeTransactions: (data) =>
    apiCall('/transactions/analyze', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // ============================================================================
  // SATELLITE DATA
  // ============================================================================
  
  /**
   * Get satellite NDVI data
   */
  getSatelliteData: (coordinates, dateRange) =>
    apiCall('/satellite/ndvi', {
      method: 'POST',
      body: JSON.stringify({ coordinates, date_range: dateRange }),
    }),

  // ============================================================================
  // WEATHER DATA
  // ============================================================================
  
  /**
   * Get weather risk assessment
   */
  getWeatherRisk: (coordinates, dateRange) =>
    apiCall('/weather/risk', {
      method: 'POST',
      body: JSON.stringify({ coordinates, date_range: dateRange }),
    }),
};

export default api;