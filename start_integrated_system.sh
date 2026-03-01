#!/bin/bash

# GramScore AI - Integrated System Startup Script
# Starts both Frontend and Backend together

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          🌾 GramScore AI - Integrated System 🌾              ║"
echo "║                                                              ║"
echo "║        AI-Driven Credit Identity for Rural Bharat           ║"
echo "║              AWS AI Bharat Hackathon 2024                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites met!${NC}"
echo ""

# Install Python dependencies
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
cd gramscore_prototype
pip3 install -q -r requirements.txt
cd ..
echo -e "${GREEN}✅ Python dependencies installed${NC}"
echo ""

# Install Node dependencies
echo -e "${BLUE}📦 Installing Node dependencies...${NC}"
cd gramscore-frontend
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "Node modules already installed"
fi
cd ..
echo -e "${GREEN}✅ Node dependencies installed${NC}"
echo ""

# Create log directory
mkdir -p logs

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🚀 Starting Services                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Start Flask API Backend
echo -e "${BLUE}🔧 Starting Flask API Backend...${NC}"
cd gramscore_prototype
python3 api_server.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
echo -e "   📡 API: http://localhost:5000/api"
echo -e "   📊 Health: http://localhost:5000/api/health"
echo ""

# Wait for backend to start
echo -e "${YELLOW}⏳ Waiting for backend to initialize...${NC}"
sleep 5

# Check if backend is running
if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is healthy!${NC}"
else
    echo -e "${YELLOW}⚠️  Backend may still be starting...${NC}"
fi
echo ""

# Start React Frontend
echo -e "${BLUE}🎨 Starting React Frontend...${NC}"
cd gramscore-frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
echo -e "   🌐 URL: http://localhost:5173"
echo ""

# Wait for frontend to start
echo -e "${YELLOW}⏳ Waiting for frontend to initialize...${NC}"
sleep 5
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  ✅ System Ready!                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}🎯 Access Points:${NC}"
echo -e "   🌐 React Frontend:    ${BLUE}http://localhost:5173${NC}"
echo -e "   📡 Flask API:         ${BLUE}http://localhost:5000/api${NC}"
echo -e "   🎯 Streamlit Demo:    ${BLUE}http://localhost:8501${NC} (if running)"
echo ""
echo -e "${GREEN}📊 Features Available:${NC}"
echo -e "   ✅ Real-time credit scoring"
echo -e "   ✅ AWS ML integration (Bedrock, SageMaker)"
echo -e "   ✅ Multi-language support (English, Hindi, Marathi)"
echo -e "   ✅ Satellite data analysis"
echo -e "   ✅ Transaction pattern analysis"
echo -e "   ✅ Voice-based assessment"
echo ""
echo -e "${GREEN}📝 Logs:${NC}"
echo -e "   Backend:  ${BLUE}tail -f logs/backend.log${NC}"
echo -e "   Frontend: ${BLUE}tail -f logs/frontend.log${NC}"
echo ""
echo -e "${YELLOW}⚠️  Press Ctrl+C to stop all services${NC}"
echo ""

# Save PIDs to file for cleanup
echo "$BACKEND_PID" > logs/backend.pid
echo "$FRONTEND_PID" > logs/frontend.pid

# Wait for user interrupt
trap "echo ''; echo -e '${YELLOW}🛑 Stopping services...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f logs/*.pid; echo -e '${GREEN}✅ All services stopped${NC}'; exit 0" INT

# Keep script running
wait