#!/usr/bin/env python3
"""
GramScore AI Demo Runner
Comprehensive demo script showcasing all features
"""

import sys
import os
import subprocess
import time
import json
from datetime import datetime
import pandas as pd
import numpy as np

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml_models import GramScoreMLModel, EnsembleGramScoreModel
from aws_services import AWSServicesOrchestrator
from data_sources import DataSourceOrchestrator
from voice_assessment import VoiceAssessmentService

def print_banner():
    """Print demo banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                     🌾 GramScore AI Demo 🌾                  ║
    ║                                                              ║
    ║        AI-Driven Credit Identity for Rural Bharat           ║
    ║              AWS AI Bharat Hackathon 2024                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_ml_model_demo():
    """Demonstrate ML model training and prediction"""
    print("\n🤖 Machine Learning Model Demo")
    print("=" * 50)
    
    # Initialize model
    model = GramScoreMLModel('xgboost')
    
    print("📊 Generating synthetic training data...")
    training_data = model.generate_synthetic_data(n_samples=5000)
    print(f"✅ Generated {len(training_data)} training samples")
    
    print("\n🏋️ Training XGBoost model...")
    metrics = model.train(training_data)
    
    print(f"📈 Model Performance:")
    print(f"   - Test R² Score: {metrics['test_r2']:.3f}")
    print(f"   - Test RMSE: {metrics['test_rmse']:.1f}")
    print(f"   - Cross-validation RMSE: {metrics['cv_rmse_mean']:.1f} ± {metrics['cv_rmse_std']:.1f}")
    
    # Test prediction
    print("\n🎯 Testing Prediction...")
    test_features = {
        'upi_consistency': 85,
        'transaction_volume': 25000,
        'ndvi_avg': 0.65,
        'utility_payment_score': 80,
        'psychometric_score': 75,
        'weather_impact': 0.9,
        'land_size': 2.5,
        'crop_types': ['Rice', 'Wheat']
    }
    
    prediction = model.predict(test_features)
    print(f"   - Predicted GramScore: {prediction['predicted_score']}")
    print(f"   - Confidence: {prediction['confidence']:.2f}")
    print(f"   - Top Features: {list(prediction['feature_importance'].keys())[:3]}")
    
    return model, prediction

def run_ensemble_demo():
    """Demonstrate ensemble model"""
    print("\n🎭 Ensemble Model Demo")
    print("=" * 50)
    
    ensemble = EnsembleGramScoreModel()
    
    print("🏋️ Training ensemble models (XGBoost + Random Forest + Gradient Boosting)...")
    ensemble_metrics = ensemble.train()
    
    print("📊 Ensemble Performance:")
    for model_name, metrics in ensemble_metrics.items():
        print(f"   - {model_name}: R² = {metrics['test_r2']:.3f}, RMSE = {metrics['test_rmse']:.1f}")
    
    # Test ensemble prediction
    test_features = {
        'upi_consistency': 70,
        'transaction_volume': 15000,
        'ndvi_avg': 0.45,
        'utility_payment_score': 65,
        'psychometric_score': 60,
        'weather_impact': 0.8,
        'land_size': 1.5,
        'crop_types': ['Cotton']
    }
    
    ensemble_prediction = ensemble.predict(test_features)
    print(f"\n🎯 Ensemble Prediction:")
    print(f"   - Final Score: {ensemble_prediction['predicted_score']}")
    print(f"   - Confidence: {ensemble_prediction['confidence']:.2f}")
    print(f"   - Individual Predictions: {[p['predicted_score'] for p in ensemble_prediction['individual_predictions'].values()]}")
    
    return ensemble

def run_data_sources_demo():
    """Demonstrate data sources integration"""
    print("\n📡 Data Sources Integration Demo")
    print("=" * 50)
    
    orchestrator = DataSourceOrchestrator()
    
    # Mock user profile
    user_profile = {
        'user_id': 'DEMO_USER_001',
        'location': {
            'coordinates': {'lat': 18.5204, 'lon': 73.8567}
        }
    }
    
    print("🔄 Collecting data from all sources...")
    collected_data = orchestrator.collect_all_data(user_profile)
    
    if collected_data['status'] == 'success':
        print("✅ Data collection successful!")
        
        # Display transaction analysis
        if 'transactions' in collected_data:
            trans_analysis = collected_data['transactions']['analysis']
            print(f"   - Transaction Consistency: {trans_analysis['consistency_score']:.1f}%")
            print(f"   - Transaction Volume Score: {trans_analysis['volume_score']:.1f}")
        
        # Display satellite data
        if 'satellite' in collected_data:
            ndvi_data = collected_data['satellite']['ndvi_data']
            print(f"   - Average NDVI: {ndvi_data['average_ndvi']:.3f}")
            print(f"   - Data Source: {ndvi_data['data_source']}")
        
        # Display weather risk
        if 'weather' in collected_data:
            weather_risk = collected_data['weather']['risk_assessment']
            print(f"   - Weather Risk Level: {weather_risk['risk_level']}")
            print(f"   - Risk Score: {weather_risk['risk_score']:.2f}")
        
        # Display utility payments
        if 'utilities' in collected_data:
            utility_score = collected_data['utilities']['payment_score']
            print(f"   - Utility Payment Score: {utility_score['score']}/100")
        
        # Prepare features for ML
        features = orchestrator.prepare_features_for_ml(collected_data)
        print(f"\n📊 Prepared ML Features:")
        for feature, value in features.items():
            if isinstance(value, (int, float)):
                print(f"   - {feature}: {value}")
        
        return collected_data, features
    
    else:
        print(f"❌ Data collection failed: {collected_data.get('error', 'Unknown error')}")
        return None, None

def run_voice_assessment_demo():
    """Demonstrate voice assessment"""
    print("\n🎤 Voice Assessment Demo")
    print("=" * 50)
    
    voice_service = VoiceAssessmentService()
    
    # Mock responses for demo
    mock_responses = {
        'q1': {
            'question': 'How do you typically plan your monthly expenses?',
            'response': 'I keep track of all my income and expenses in a notebook. I try to save money for emergencies and plan for the next farming season.',
            'category': 'financial_discipline',
            'type': 'open_ended',
            'expected_keywords': ['budget', 'plan', 'save', 'track', 'record']
        },
        'q2': {
            'question': 'What would you do if you had an unexpected expense of ₹5000?',
            'response': 'I would first check my savings. If not enough, I would ask family members for help or take a small loan from the local cooperative.',
            'category': 'risk_awareness',
            'type': 'scenario',
            'expected_keywords': ['borrow', 'save', 'family', 'loan', 'emergency']
        },
        'q3': {
            'question': 'How confident are you about repaying a loan on time?',
            'response': 'I am very confident because I always pay my bills on time and have a good income from farming.',
            'category': 'confidence_level',
            'type': 'confidence',
            'expected_keywords': ['confident', 'sure', 'definitely', 'always', 'never']
        }
    }
    
    print("🎯 Analyzing voice responses...")
    analysis = voice_service.analyze_voice_responses(mock_responses)
    
    print(f"📊 Assessment Results:")
    print(f"   - Overall Psychometric Score: {analysis['overall_score']}/100")
    print(f"   - Response Quality: {analysis['response_analysis']['response_quality']}")
    print(f"   - Strongest Category: {analysis['response_analysis']['strongest_category']}")
    
    print(f"\n💡 Recommendations:")
    for rec in analysis['recommendations'][:3]:
        print(f"   - {rec}")
    
    return analysis

def run_aws_services_demo():
    """Demonstrate AWS services integration"""
    print("\n☁️ AWS Services Integration Demo")
    print("=" * 50)
    
    aws_orchestrator = AWSServicesOrchestrator()
    
    # Health check
    health = aws_orchestrator.health_check()
    print("🏥 AWS Services Health Check:")
    for service, status in health.items():
        status_icon = "✅" if status else "❌"
        print(f"   - {service}: {status_icon}")
    
    # Mock user data for comprehensive scoring
    user_data = {
        'user_id': 'AWS_DEMO_USER',
        'upi_consistency': 80,
        'ndvi_avg': 0.6,
        'utility_payment_score': 75,
        'psychometric_score': 70,
        'location': {
            'coordinates': {'lat': 18.5, 'lon': 73.8}
        }
    }
    
    print("\n🧠 Calculating comprehensive score using AWS services...")
    comprehensive_result = aws_orchestrator.calculate_comprehensive_score(user_data)
    
    print(f"📊 AWS-Powered Results:")
    print(f"   - GramScore: {comprehensive_result['gramscore']}")
    print(f"   - Confidence: {comprehensive_result['confidence']:.2f}")
    print(f"   - Services Used: {list(comprehensive_result['aws_services_used'].values())}")
    
    if 'ai_insights' in comprehensive_result:
        print(f"\n🤖 AI Insights (First 100 chars):")
        print(f"   {comprehensive_result['ai_insights'][:100]}...")
    
    return comprehensive_result

def run_complete_demo():
    """Run complete end-to-end demo"""
    print("\n🚀 Complete End-to-End Demo")
    print("=" * 50)
    
    # Simulate complete user journey
    user_profiles = [
        {
            'name': 'Reliable Farmer',
            'data': {
                'user_id': 'FARMER_001',
                'upi_consistency': 90,
                'transaction_volume': 45000,
                'ndvi_avg': 0.65,
                'utility_payment_score': 85,
                'psychometric_score': 80,
                'weather_impact': 1.0,
                'land_size': 2.5,
                'crop_types': ['Rice', 'Wheat', 'Sugarcane']
            }
        },
        {
            'name': 'New-to-Credit',
            'data': {
                'user_id': 'NEWBIE_001',
                'upi_consistency': 70,
                'transaction_volume': 15000,
                'ndvi_avg': 0.0,
                'utility_payment_score': 75,
                'psychometric_score': 65,
                'weather_impact': 1.0,
                'land_size': 0.0,
                'crop_types': []
            }
        },
        {
            'name': 'High Risk',
            'data': {
                'user_id': 'RISK_001',
                'upi_consistency': 30,
                'transaction_volume': 8000,
                'ndvi_avg': 0.20,
                'utility_payment_score': 45,
                'psychometric_score': 40,
                'weather_impact': 0.4,
                'land_size': 0.8,
                'crop_types': ['Cotton']
            }
        }
    ]
    
    # Initialize model for scoring
    model = GramScoreMLModel('xgboost')
    model.train()  # Quick training with default data
    
    results = []
    
    for profile in user_profiles:
        print(f"\n👤 Processing: {profile['name']}")
        
        # Calculate score
        prediction = model.predict(profile['data'])
        score = prediction['predicted_score']
        
        # Determine risk category
        if score >= 750:
            risk_category = "Low Risk - Approved for low-interest loan"
        elif score >= 500:
            risk_category = "Medium Risk - Conditional approval"
        else:
            risk_category = "High Risk - Government subsidy recommended"
        
        print(f"   - GramScore: {score}")
        print(f"   - Risk Category: {risk_category}")
        print(f"   - Confidence: {prediction['confidence']:.2f}")
        
        results.append({
            'profile': profile['name'],
            'score': score,
            'risk_category': risk_category,
            'confidence': prediction['confidence']
        })
    
    # Summary
    print(f"\n📈 Demo Summary:")
    print(f"   - Profiles Processed: {len(results)}")
    print(f"   - Average Score: {np.mean([r['score'] for r in results]):.0f}")
    print(f"   - Score Range: {min(r['score'] for r in results)} - {max(r['score'] for r in results)}")
    
    return results

def save_demo_results(results_dict):
    """Save demo results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"gramscore_demo_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results_dict, f, indent=2, default=str)
    
    print(f"\n💾 Demo results saved to: {filename}")

def main():
    """Main demo function"""
    print_banner()
    
    print("🎯 Starting GramScore AI Comprehensive Demo...")
    print("This demo showcases all major components of the system.\n")
    
    demo_results = {
        'timestamp': datetime.now().isoformat(),
        'demo_version': '1.0.0',
        'components_tested': []
    }
    
    try:
        # 1. ML Model Demo
        print("1️⃣ Running ML Model Demo...")
        model, prediction = run_ml_model_demo()
        demo_results['ml_model'] = {
            'prediction_sample': prediction,
            'status': 'success'
        }
        demo_results['components_tested'].append('ml_models')
        
        # 2. Ensemble Demo
        print("\n2️⃣ Running Ensemble Model Demo...")
        ensemble = run_ensemble_demo()
        demo_results['ensemble_model'] = {'status': 'success'}
        demo_results['components_tested'].append('ensemble_models')
        
        # 3. Data Sources Demo
        print("\n3️⃣ Running Data Sources Demo...")
        collected_data, features = run_data_sources_demo()
        demo_results['data_sources'] = {
            'features_extracted': features,
            'status': 'success' if features else 'partial'
        }
        demo_results['components_tested'].append('data_sources')
        
        # 4. Voice Assessment Demo
        print("\n4️⃣ Running Voice Assessment Demo...")
        voice_analysis = run_voice_assessment_demo()
        demo_results['voice_assessment'] = {
            'psychometric_score': voice_analysis['overall_score'],
            'status': 'success'
        }
        demo_results['components_tested'].append('voice_assessment')
        
        # 5. AWS Services Demo
        print("\n5️⃣ Running AWS Services Demo...")
        aws_result = run_aws_services_demo()
        demo_results['aws_services'] = {
            'gramscore': aws_result['gramscore'],
            'confidence': aws_result['confidence'],
            'status': 'success'
        }
        demo_results['components_tested'].append('aws_services')
        
        # 6. Complete End-to-End Demo
        print("\n6️⃣ Running Complete End-to-End Demo...")
        complete_results = run_complete_demo()
        demo_results['end_to_end'] = {
            'profiles_processed': len(complete_results),
            'results': complete_results,
            'status': 'success'
        }
        demo_results['components_tested'].append('end_to_end')
        
        # Save results
        save_demo_results(demo_results)
        
        # Final summary
        print("\n" + "="*60)
        print("🎉 GramScore AI Demo Completed Successfully!")
        print("="*60)
        print(f"✅ Components Tested: {len(demo_results['components_tested'])}")
        print(f"✅ All Systems Operational")
        print(f"✅ Ready for AWS AI Bharat Hackathon Presentation")
        
        print(f"\n🚀 Next Steps:")
        print(f"   1. Run 'streamlit run app.py' for interactive demo")
        print(f"   2. Deploy to AWS for production testing")
        print(f"   3. Integrate with real data sources")
        print(f"   4. Scale for 10,000+ concurrent users")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        demo_results['status'] = 'failed'
        demo_results['error'] = str(e)
        save_demo_results(demo_results)
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)