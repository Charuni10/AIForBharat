#!/bin/bash

# GramScore AI Demo Startup Script
# AWS AI Bharat Hackathon 2024

echo "🌾 Starting GramScore AI Demo..."
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Run comprehensive demo first
echo "🚀 Running comprehensive demo..."
python run_demo.py

# Check if demo was successful
if [ $? -eq 0 ]; then
    echo "✅ Demo completed successfully!"
    echo ""
    echo "🌐 Starting Streamlit web application..."
    echo "📱 Open your browser to: http://localhost:8501"
    echo ""
    echo "🎯 Demo Features:"
    echo "   • Multi-language support (English, Hindi, Marathi)"
    echo "   • AWS services integration (Bedrock, SageMaker)"
    echo "   • Real-time credit scoring"
    echo "   • Satellite data analysis"
    echo "   • Voice-based assessment"
    echo ""
    echo "Press Ctrl+C to stop the application"
    echo ""
    
    # Start Streamlit app
    streamlit run app.py
else
    echo "❌ Demo failed. Please check the error messages above."
    exit 1
fi