"""
GramScore AI - Flask API Server
REST API backend for React frontend integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from functools import wraps
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml_models import GramScoreMLModel
from aws_services import AWSServicesOrchestrator
from data_sources import DataSourceOrchestrator
from voice_assessment import VoiceAssessmentService

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
app.config['SECRET_KEY'] = 'gramscore-secret-key-change-in-production'
app.config['JWT_EXPIRATION_HOURS'] = 24

# Initialize services
print("🚀 Initializing GramScore AI services...")
ml_model = GramScoreMLModel('xgboost')
print("📊 Training ML model...")
ml_model.train()
print("✅ ML model trained successfully!")

aws_services = AWSServicesOrchestrator()
data_orchestrator = DataSourceOrchestrator()
voice_service = VoiceAssessmentService()

print("✅ All services initialized!")

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorator

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'services': {
            'ml_model': ml_model.is_trained,
            'aws_services': aws_services.health_check(),
            'data_sources': 'operational',
            'voice_assessment': 'operational'
        }
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User authentication endpoint"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    user_id = data.get('user_id')
    phone = data.get('phone')
    
    if not user_id or not phone:
        return jsonify({'error': 'user_id and phone are required'}), 400
    
    # In production, verify credentials against database
    # For demo, generate token directly
    token = jwt.encode({
        'user_id': user_id,
        'phone': phone,
        'exp': datetime.utcnow() + timedelta(hours=app.config['JWT_EXPIRATION_HOURS'])
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'success': True,
        'token': token,
        'user_id': user_id,
        'expires_in': app.config['JWT_EXPIRATION_HOURS'] * 3600,
        'message': 'Login successful'
    })

@app.route('/api/consent', methods=['POST'])
@token_required
def submit_consent(current_user):
    """Submit user consent for data access"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    consent_data = {
        'user_id': current_user,
        'data_types': data.get('data_types', []),
        'timestamp': datetime.now().isoformat(),
        'consent_given': True,
        'validity_days': 90
    }
    
    # In production, store consent in DynamoDB
    consent_token = f'consent_{current_user}_{int(datetime.now().timestamp())}'
    
    return jsonify({
        'success': True,
        'consent_token': consent_token,
        'consent_data': consent_data,
        'message': 'Consent recorded successfully'
    })

@app.route('/api/data/collect', methods=['POST'])
@token_required
def collect_user_data(current_user):
    """Collect data from all sources"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    user_profile = {
        'user_id': current_user,
        'location': data.get('location', {
            'coordinates': {'lat': 18.5204, 'lon': 73.8567}
        })
    }
    
    # Collect data from all sources
    collected_data = data_orchestrator.collect_all_data(user_profile)
    
    # Prepare features for ML
    features = data_orchestrator.prepare_features_for_ml(collected_data)
    
    return jsonify({
        'success': True,
        'data': collected_data,
        'features': features,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/score/calculate', methods=['POST'])
@token_required
def calculate_score(current_user):
    """Calculate GramScore"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
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
    features['user_id'] = current_user
    aws_result = aws_services.calculate_comprehensive_score(features)
    
    # Determine risk level
    score = prediction['predicted_score']
    if score >= 750:
        risk_level = 'Low'
        recommendation = 'Approved for low-interest micro-loan'
    elif score >= 500:
        risk_level = 'Medium'
        recommendation = 'Conditional approval with monitoring'
    else:
        risk_level = 'High'
        recommendation = 'Government subsidy recommended'
    
    return jsonify({
        'success': True,
        'gramscore': score,
        'confidence': prediction['confidence'],
        'components': prediction['feature_importance'],
        'ai_insights': aws_result.get('ai_insights', 'Score calculated successfully'),
        'risk_level': risk_level,
        'recommendation': recommendation,
        'timestamp': datetime.now().isoformat(),
        'model_type': prediction['model_type']
    })

@app.route('/api/score/history/<user_id>', methods=['GET'])
@token_required
def get_score_history(current_user, user_id):
    """Get user's score history"""
    
    # Verify user can only access their own history
    if current_user != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # In production, fetch from DynamoDB
    # For demo, return mock historical data
    history = [
        {
            'score': 720,
            'date': '2024-02-15',
            'risk_level': 'Low',
            'components': {
                'transaction_frequency': 85,
                'agricultural_productivity': 70,
                'utility_payments': 75,
                'psychometric_score': 80
            }
        },
        {
            'score': 680,
            'date': '2024-01-15',
            'risk_level': 'Medium',
            'components': {
                'transaction_frequency': 75,
                'agricultural_productivity': 65,
                'utility_payments': 70,
                'psychometric_score': 75
            }
        }
    ]
    
    return jsonify({
        'success': True,
        'user_id': user_id,
        'scores': history,
        'count': len(history)
    })

@app.route('/api/voice/assess', methods=['POST'])
@token_required
def voice_assessment(current_user):
    """Process voice assessment"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    responses = data.get('responses', {})
    language = data.get('language', 'english')
    
    if not responses:
        return jsonify({'error': 'No responses provided'}), 400
    
    # Process voice assessment
    analysis = voice_service.analyze_voice_responses(responses, language)
    
    return jsonify({
        'success': True,
        'psychometric_score': analysis['overall_score'],
        'category_scores': analysis['category_scores'],
        'recommendations': analysis['recommendations'],
        'response_analysis': analysis['response_analysis'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/transactions/analyze', methods=['POST'])
@token_required
def analyze_transactions(current_user):
    """Analyze transaction patterns"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Get transaction data
    from data_sources import AccountAggregatorService
    aa_service = AccountAggregatorService()
    
    consent_token = data.get('consent_token')
    date_range = data.get('date_range', (
        (datetime.now() - timedelta(days=90)).isoformat(),
        datetime.now().isoformat()
    ))
    
    transactions_df = aa_service.fetch_transaction_data(consent_token, date_range)
    analysis = aa_service.analyze_transaction_patterns(transactions_df)
    
    return jsonify({
        'success': True,
        'analysis': analysis,
        'transaction_count': len(transactions_df),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/satellite/ndvi', methods=['POST'])
@token_required
def get_satellite_data(current_user):
    """Get satellite NDVI data"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    coordinates = data.get('coordinates', {'lat': 18.5204, 'lon': 73.8567})
    date_range = data.get('date_range', (
        (datetime.now() - timedelta(days=365)).isoformat(),
        datetime.now().isoformat()
    ))
    
    from data_sources import SatelliteDataService
    satellite_service = SatelliteDataService()
    
    ndvi_data = satellite_service.get_ndvi_data(coordinates, date_range)
    land_validation = satellite_service.validate_land_coordinates(coordinates)
    
    return jsonify({
        'success': True,
        'ndvi_data': ndvi_data,
        'land_validation': land_validation,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/weather/risk', methods=['POST'])
@token_required
def get_weather_risk(current_user):
    """Get weather risk assessment"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    coordinates = data.get('coordinates', {'lat': 18.5204, 'lon': 73.8567})
    date_range = data.get('date_range', (
        (datetime.now() - timedelta(days=365)).isoformat(),
        datetime.now().isoformat()
    ))
    
    from data_sources import WeatherDataService
    weather_service = WeatherDataService()
    
    weather_data = weather_service.get_weather_history(coordinates, date_range)
    
    return jsonify({
        'success': True,
        'weather_data': weather_data,
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌾 GramScore AI - Flask API Server")
    print("="*60)
    print("📡 Server starting on http://localhost:5001")
    print("📚 API Documentation: http://localhost:5001/api/health")
    print("🔗 React Frontend: http://localhost:5174")
    print("🎯 Streamlit Demo: http://localhost:8501")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)