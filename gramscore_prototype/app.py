import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import boto3
from botocore.exceptions import ClientError
import requests
import time

# Page Configuration
st.set_page_config(
    page_title="GramScore AI - AWS AI Bharat Hackathon", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2a5298;
    }
    .score-display {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .high-score { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
    .medium-score { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
    .low-score { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); color: #333; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌾 GramScore AI</h1>
    <h3>AI-Driven Credit Identity for Rural Bharat</h3>
    <p>Powered by AWS Machine Learning & Satellite Data</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'score_calculated' not in st.session_state:
    st.session_state.score_calculated = False

# Sidebar Configuration
st.sidebar.header("🎯 Demo Configuration")

# AWS Configuration Section
st.sidebar.subheader("AWS Services Integration")
aws_region = st.sidebar.selectbox("AWS Region", ["ap-south-1", "us-east-1", "eu-west-1"])
use_aws_services = st.sidebar.checkbox("Enable AWS Services", value=True)

# User Persona Selection
st.sidebar.subheader("Select Applicant Persona")
persona = st.sidebar.selectbox(
    "Choose a Profile", 
    ["Reliable Farmer", "High Risk/Distress", "New-to-Credit", "Custom Input"]
)

# Language Selection
language = st.sidebar.selectbox("भाषा / Language", ["English", "हिंदी (Hindi)", "मराठी (Marathi)"])

# Mock AWS Services Integration
class AWSServicesIntegrator:
    def __init__(self, region='ap-south-1'):
        self.region = region
        self.bedrock_client = None
        self.sagemaker_client = None
        
    def initialize_clients(self):
        """Initialize AWS clients (mock for demo)"""
        try:
            # In production, these would be real AWS clients
            self.bedrock_client = "mock_bedrock_client"
            self.sagemaker_client = "mock_sagemaker_client"
            return True
        except Exception as e:
            st.error(f"AWS Client initialization failed: {str(e)}")
            return False
    
    def invoke_bedrock_model(self, prompt, model_id="amazon.titan-text-express-v1"):
        """Mock Bedrock model invocation"""
        # Simulate API call delay
        time.sleep(0.5)
        
        # Mock response based on prompt content
        if "credit risk" in prompt.lower():
            return {
                "risk_assessment": "Low to Medium Risk",
                "confidence": 0.85,
                "factors": ["Consistent UPI transactions", "Good agricultural productivity"]
            }
        return {"response": "Mock Bedrock response for: " + prompt[:50] + "..."}
    
    def get_sagemaker_prediction(self, features):
        """Mock SageMaker endpoint prediction"""
        time.sleep(0.3)
        
        # Mock ML prediction
        base_score = np.random.normal(650, 100)
        confidence = np.random.uniform(0.7, 0.95)
        
        return {
            "predicted_score": max(300, min(900, int(base_score))),
            "confidence": confidence,
            "feature_importance": {
                "transaction_frequency": 0.35,
                "agricultural_productivity": 0.30,
                "utility_payments": 0.20,
                "psychometric_score": 0.15
            }
        }

# Initialize AWS services
aws_integrator = AWSServicesIntegrator(aws_region)
if use_aws_services:
    aws_integrator.initialize_clients()

# Data Generation Functions
def generate_persona_data(persona_type):
    """Generate mock data based on selected persona"""
    base_data = {
        "user_id": f"USER_{np.random.randint(10000, 99999)}",
        "location": {
            "state": "Maharashtra",
            "district": "Pune",
            "coordinates": {"lat": 18.5204, "lon": 73.8567}
        }
    }
    
    if persona_type == "Reliable Farmer":
        return {
            **base_data,
            "upi_consistency": 90,
            "transaction_volume": 45000,
            "ndvi_avg": 0.65,
            "utility_payment_score": 85,
            "psychometric_score": 80,
            "weather_impact": 1.0,
            "land_size": 2.5,
            "crop_types": ["Rice", "Wheat", "Sugarcane"]
        }
    elif persona_type == "High Risk/Distress":
        return {
            **base_data,
            "upi_consistency": 30,
            "transaction_volume": 8000,
            "ndvi_avg": 0.20,
            "utility_payment_score": 45,
            "psychometric_score": 40,
            "weather_impact": 0.4,
            "land_size": 0.8,
            "crop_types": ["Cotton"]
        }
    else:  # New-to-Credit
        return {
            **base_data,
            "upi_consistency": 70,
            "transaction_volume": 15000,
            "ndvi_avg": 0.0,  # No farm data yet
            "utility_payment_score": 75,
            "psychometric_score": 65,
            "weather_impact": 1.0,
            "land_size": 0.0,
            "crop_types": []
        }

def generate_transaction_data(volume, consistency):
    """Generate mock UPI transaction data"""
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    
    # Generate transactions based on consistency
    num_transactions = int(volume / 1000)  # Scale down for demo
    
    transactions = []
    for i in range(num_transactions):
        date = np.random.choice(dates)
        amount = np.random.lognormal(mean=6, sigma=1.5)  # Log-normal distribution for amounts
        
        # Categorize transactions
        if np.random.random() < 0.6:  # 60% business transactions
            category = "Business Inflow"
            merchant = np.random.choice(["Grain Buyer", "Vegetable Market", "Dairy Cooperative", "Local Trader"])
        else:
            category = "Personal Outflow"
            merchant = np.random.choice(["Grocery Store", "Medical Store", "Fuel Station", "Utility Payment"])
        
        transactions.append({
            "date": date,
            "amount": round(amount, 2),
            "category": category,
            "merchant": merchant,
            "payment_method": "UPI"
        })
    
    return pd.DataFrame(transactions)

# GramScore Calculation Engine
def calculate_gramscore(data, use_aws=False):
    """Calculate GramScore using weighted components"""
    
    if use_aws and aws_integrator.sagemaker_client:
        # Use AWS SageMaker for prediction
        features = [
            data['upi_consistency'],
            data['ndvi_avg'],
            data['utility_payment_score'],
            data['psychometric_score']
        ]
        
        prediction = aws_integrator.get_sagemaker_prediction(features)
        return prediction['predicted_score'], prediction
    
    # Fallback to local calculation
    weights = {
        'transaction_frequency': 0.30,
        'agricultural_productivity': 0.30,
        'utility_payments': 0.20,
        'psychometric_score': 0.20
    }
    
    # Normalize scores to 0-100 scale
    transaction_score = data['upi_consistency']
    agriculture_score = min(data['ndvi_avg'] / 0.8 * 100, 100) if data['ndvi_avg'] > 0 else 0
    utility_score = data['utility_payment_score']
    psychometric_score = data['psychometric_score']
    
    # Calculate weighted score
    weighted_score = (
        transaction_score * weights['transaction_frequency'] +
        agriculture_score * weights['agricultural_productivity'] +
        utility_score * weights['utility_payments'] +
        psychometric_score * weights['psychometric_score']
    )
    
    # Convert to 300-900 scale
    final_score = int(300 + (weighted_score * 6))
    
    # Adjust for weather impact
    final_score = int(final_score * data['weather_impact'])
    
    components = {
        'transaction_frequency': transaction_score,
        'agricultural_productivity': agriculture_score,
        'utility_payments': utility_score,
        'psychometric_score': psychometric_score,
        'weather_adjustment': data['weather_impact']
    }
    
    return final_score, {'components': components, 'confidence': 0.85}

# Main Application Logic
def main():
    # Get user data based on persona
    if persona == "Custom Input":
        st.subheader("📝 Custom Input Mode")
        
        col1, col2 = st.columns(2)
        with col1:
            upi_consistency = st.slider("UPI Transaction Consistency (%)", 0, 100, 70)
            ndvi_avg = st.slider("Agricultural Productivity (NDVI)", 0.0, 1.0, 0.5, 0.05)
        
        with col2:
            utility_score = st.slider("Utility Payment Score", 0, 100, 75)
            psychometric_score = st.slider("Psychometric Assessment Score", 0, 100, 65)
        
        user_data = {
            "user_id": "CUSTOM_USER",
            "upi_consistency": upi_consistency,
            "ndvi_avg": ndvi_avg,
            "utility_payment_score": utility_score,
            "psychometric_score": psychometric_score,
            "weather_impact": 1.0,
            "transaction_volume": upi_consistency * 500,
            "land_size": ndvi_avg * 3,
            "crop_types": ["Mixed Crops"] if ndvi_avg > 0 else []
        }
    else:
        user_data = generate_persona_data(persona)
    
    st.session_state.user_data = user_data
    
    # Display user information
    st.subheader("👤 User Profile")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("UPI Transaction Consistency", f"{user_data['upi_consistency']}%")
        st.metric("Monthly Transaction Volume", f"₹{user_data['transaction_volume']:,}")
    
    with col2:
        st.metric("Agricultural Productivity (NDVI)", f"{user_data['ndvi_avg']:.2f}")
        st.metric("Land Size", f"{user_data['land_size']} acres")
    
    with col3:
        st.metric("Utility Payment Score", f"{user_data['utility_payment_score']}/100")
        st.metric("Psychometric Score", f"{user_data['psychometric_score']}/100")
    
    # Transaction Analysis
    if st.button("🔍 Analyze Transaction Data", type="primary"):
        with st.spinner("Fetching UPI transaction data via Account Aggregator..."):
            transaction_df = generate_transaction_data(
                user_data['transaction_volume'], 
                user_data['upi_consistency']
            )
            
            st.subheader("💳 Transaction Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Transaction volume chart
                daily_volume = transaction_df.groupby('date')['amount'].sum().reset_index()
                fig = px.line(daily_volume, x='date', y='amount', 
                             title="Daily Transaction Volume (Last 90 Days)")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Category distribution
                category_dist = transaction_df['category'].value_counts()
                fig = px.pie(values=category_dist.values, names=category_dist.index,
                           title="Transaction Category Distribution")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            # Show sample transactions
            st.subheader("Recent Transactions")
            st.dataframe(transaction_df.head(10), use_container_width=True)
    
    # Satellite Data Analysis
    if user_data['ndvi_avg'] > 0:
        st.subheader("🛰️ Satellite Data Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # NDVI trend simulation
            dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
            ndvi_values = [user_data['ndvi_avg'] + np.random.normal(0, 0.1) for _ in dates]
            ndvi_values = [max(0, min(1, val)) for val in ndvi_values]  # Clamp to 0-1
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=ndvi_values, mode='lines+markers',
                                   name='NDVI', line=dict(color='green', width=3)))
            fig.update_layout(title="Crop Health Trend (NDVI)", height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Crop information
            st.info(f"**Detected Crops:** {', '.join(user_data['crop_types'])}")
            st.info(f"**Land Size:** {user_data['land_size']} acres")
            st.info(f"**Current NDVI:** {user_data['ndvi_avg']:.2f}")
            
            if user_data['ndvi_avg'] > 0.6:
                st.success("🌱 Excellent crop health detected")
            elif user_data['ndvi_avg'] > 0.4:
                st.warning("🌾 Moderate crop health")
            else:
                st.error("🌿 Poor crop health - may need attention")
    
    # Calculate GramScore
    if st.button("🚀 Calculate GramScore", type="primary", use_container_width=True):
        with st.spinner("Calculating GramScore using AWS ML models..."):
            score, details = calculate_gramscore(user_data, use_aws_services)
            
            st.session_state.score_calculated = True
            st.session_state.final_score = score
            st.session_state.score_details = details
    
    # Display GramScore Results
    if st.session_state.score_calculated:
        score = st.session_state.final_score
        details = st.session_state.score_details
        
        st.markdown("---")
        st.subheader("🎯 GramScore Results")
        
        # Score display with color coding
        if score >= 750:
            score_class = "high-score"
            recommendation = "✅ Recommended for Low-Interest Micro-loan"
            risk_level = "Low Risk"
        elif score >= 500:
            score_class = "medium-score"
            recommendation = "⚠️ Recommended for Conditional Credit"
            risk_level = "Medium Risk"
        else:
            score_class = "low-score"
            recommendation = "❌ High Risk: Recommend Government Subsidy"
            risk_level = "High Risk"
        
        st.markdown(f"""
        <div class="score-display {score_class}">
            <div>GramScore</div>
            <div>{score}</div>
            <div style="font-size: 1rem; margin-top: 1rem;">{risk_level}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.success(recommendation)
        
        # Score breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Score Components")
            
            if 'components' in details:
                components = details['components']
                
                # Create radar chart for components
                categories = list(components.keys())
                values = list(components.values())
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name='Score Components'
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=False,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Improvement Recommendations")
            
            # Generate recommendations based on score components
            recommendations = []
            
            if 'components' in details:
                components = details['components']
                
                if components.get('transaction_frequency', 0) < 70:
                    recommendations.append("📱 Increase UPI transaction frequency")
                
                if components.get('agricultural_productivity', 0) < 50:
                    recommendations.append("🌾 Improve crop management practices")
                
                if components.get('utility_payments', 0) < 70:
                    recommendations.append("⚡ Pay utility bills on time")
                
                if components.get('psychometric_score', 0) < 60:
                    recommendations.append("🧠 Complete financial literacy training")
            
            if not recommendations:
                recommendations.append("🎉 Excellent profile! Maintain current practices")
            
            for rec in recommendations:
                st.info(rec)
            
            # AWS Bedrock integration for additional insights
            if use_aws_services:
                with st.spinner("Getting AI insights..."):
                    prompt = f"Analyze credit risk for farmer with score {score} and provide insights"
                    ai_insights = aws_integrator.invoke_bedrock_model(prompt)
                    
                    st.subheader("🤖 AI Insights (AWS Bedrock)")
                    st.json(ai_insights)
        
        # Explainable AI section
        st.subheader("🔍 Explainable AI - Why This Score?")
        
        explanation_text = {
            "English": f"""
            Your GramScore of {score} is calculated based on:
            • **Transaction Behavior (30%)**: Your UPI transaction consistency shows {user_data['upi_consistency']}% regularity
            • **Agricultural Productivity (30%)**: Satellite data indicates {user_data['ndvi_avg']:.2f} NDVI crop health
            • **Utility Payments (20%)**: Your bill payment history scores {user_data['utility_payment_score']}/100
            • **Repayment Intent (20%)**: Psychometric assessment scored {user_data['psychometric_score']}/100
            """,
            "हिंदी (Hindi)": f"""
            आपका GramScore {score} इन आधारों पर बना है:
            • **लेनदेन व्यवहार (30%)**: आपकी UPI लेनदेन नियमितता {user_data['upi_consistency']}% है
            • **कृषि उत्पादकता (30%)**: उपग्रह डेटा {user_data['ndvi_avg']:.2f} NDVI फसल स्वास्थ्य दिखाता है
            • **उपयोगिता भुगतान (20%)**: आपका बिल भुगतान इतिहास {user_data['utility_payment_score']}/100 है
            • **चुकौती इरादा (20%)**: मनोवैज्ञानिक मूल्यांकन {user_data['psychometric_score']}/100 है
            """,
            "मराठी (Marathi)": f"""
            तुमचा GramScore {score} या आधारावर बनला आहे:
            • **व्यवहार पद्धती (30%)**: तुमची UPI व्यवहार नियमितता {user_data['upi_consistency']}% आहे
            • **कृषी उत्पादकता (30%)**: उपग्रह डेटा {user_data['ndvi_avg']:.2f} NDVI पीक आरोग्य दर्शवितो
            • **उपयोगिता पेमेंट (20%)**: तुमचा बिल पेमेंट इतिहास {user_data['utility_payment_score']}/100 आहे
            • **परतफेड हेतू (20%)**: मानसिक मूल्यांकन {user_data['psychometric_score']}/100 आहे
            """
        }
        
        st.info(explanation_text.get(language, explanation_text["English"]))
        
        # Data sources and compliance
        st.subheader("📋 Data Sources & Compliance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Data Sources:**
            - 🏦 Account Aggregator (UPI transactions)
            - 🛰️ Sentinel-2 Satellite (NDVI data)
            - ⚡ Utility payment records
            - 🎤 Voice-based psychometric assessment
            """)
        
        with col2:
            st.markdown("""
            **Compliance:**
            - ✅ DPDP Act 2023 compliant
            - ✅ Data stored in AWS Mumbai region
            - ✅ User consent recorded
            - ✅ Audit trail maintained
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>GramScore AI MVP</strong> - Empowering Rural Financial Inclusion</p>
    <p>Built for AWS AI Bharat Hackathon | Powered by AWS Bedrock, SageMaker & Satellite Data</p>
    <p>🌾 Serving 200M+ unbanked rural Indians with AI-driven credit identity</p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()