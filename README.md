# 🌾 GramScore AI

**AI-Driven Credit Identity for Rural Bharat**

GramScore AI is a revolutionary credit scoring platform that uses alternative data sources and AI/ML to provide credit scores for unbanked farmers in rural India. Built for the AWS AI Bharat Hackathon 2024.

---

## 🎯 Problem Statement

Over 100 million farmers in rural India lack access to formal credit due to the absence of traditional credit history. This creates a ₹10 trillion credit gap and limits agricultural growth and financial inclusion.

## 💡 Solution

GramScore AI generates credit scores (300-900) using:
- 📱 **UPI Transaction Data** - Digital payment patterns
- 🛰️ **Satellite Imagery** - NDVI crop health analysis
- ⚡ **Utility Payments** - Electricity and mobile bill history
- 🎤 **Voice Assessment** - AI-powered psychometric evaluation
- 🤖 **AWS AI/ML** - Bedrock, SageMaker for insights

---

## ✨ Features

### For Farmers
- 📊 Real-time credit score (300-900 scale)
- 🔐 Consent-based data collection (DPDP Act 2023 compliant)
- 🗣️ Multilingual voice assessment (6 languages)
- 🤖 AI-powered personalized recommendations
- 🏆 Gamified achievements system
- 📈 Score improvement tracking

### For Banks/Lenders
- 👥 Admin portal to view all farmers
- 🔍 Search and filter by risk level
- 📥 Export data to CSV
- 📊 Portfolio analytics
- ⚡ Automated credit decisions

### For Government
- 🎯 Target farmers for subsidy programs
- 📈 Track financial inclusion metrics
- 🌾 Monitor agricultural productivity
- 💰 Measure program impact

---

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd AIForBharat
```

2. **Install Backend Dependencies**
```bash
cd gramscore_prototype
pip3 install -r requirements.txt
cd ..
```

3. **Install Frontend Dependencies**
```bash
cd gramscore-frontend
npm install
cd ..
```

4. **Start the Application**
```bash
# Option 1: Use the startup script (recommended)
chmod +x start_integrated_system.sh
./start_integrated_system.sh

# Option 2: Start manually
# Terminal 1 - Backend
cd gramscore_prototype
python3 api_server.py

# Terminal 2 - Frontend
cd gramscore-frontend
npm run dev
```

5. **Access the Application**
- Frontend: http://localhost:5174
- Backend API: http://localhost:5001

---

## 🔐 Demo Credentials

### Farmers (5 Personas)

| Name | User ID | Password | Score | Risk Level |
|------|---------|----------|-------|------------|
| Rajesh Kumar | `rajesh_kumar_001` | `rajesh123` | 785 | Low |
| Lakshmi Reddy | `lakshmi_reddy_004` | `lakshmi123` | 720 | Low |
| Sunita Devi | `sunita_devi_002` | `sunita123` | 625 | Medium |
| Kumar Swamy | `kumar_swamy_005` | `kumar123` | 550 | Medium |
| Ramesh Patil | `ramesh_patil_003` | `ramesh123` | 485 | High |

### Admin
- Username: `admin`
- Password: `gramscore2024`

---

## 📱 User Flows

### Farmer Journey
1. **Login** → Enter farmer credentials
2. **Dashboard** → View GramScore and breakdown
3. **Data Approvals** → Consent to data sources
4. **Voice Assessment** → Answer 8 questions (chat or voice)
5. **Profile** → View AI insights and recommendations
6. **Logout** → Secure session end

### Admin Journey
1. **Login** → Enter admin credentials
2. **Admin Portal** → View all farmers
3. **Search/Filter** → Find specific farmers or risk levels
4. **View Details** → Click farmer for complete profile
5. **Export** → Download CSV for reporting
6. **Logout** → Secure session end

---

## 🏗️ Architecture

### Frontend (React + Vite)
```
gramscore-frontend/
├── src/
│   ├── components/
│   │   ├── Login.jsx           # Unified login
│   │   ├── Dashboard.jsx       # Farmer dashboard
│   │   ├── ConsentForm.jsx     # Data approvals
│   │   ├── VoiceAssessment.jsx # Chat/Voice assessment
│   │   ├── Profile.jsx         # AI insights & recommendations
│   │   ├── Admin.jsx           # Admin portal
│   │   └── Navigation.jsx      # Navigation with logout
│   ├── context/
│   │   └── LanguageContext.jsx # i18n support
│   ├── services/
│   │   └── api.js              # API integration
│   └── translations.js         # 6 languages
```

### Backend (Python Flask)
```
gramscore_prototype/
├── api_server.py          # REST API (port 5001)
├── ml_models.py           # XGBoost, RF, GB models
├── aws_services.py        # Bedrock, SageMaker, S3, DynamoDB
├── data_sources.py        # Account Aggregator, Satellite, Weather
├── voice_assessment.py    # Multilingual voice analysis
└── demo_data.py           # Mock data generator
```

---

## 🔧 Technology Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **React Router** - Navigation
- **Lucide React** - Icons
- **CSS3** - Styling with glassmorphism

### Backend
- **Flask** - REST API
- **XGBoost** - ML model
- **Pandas** - Data processing
- **NumPy** - Numerical computing

### AWS Services
- **Amazon Bedrock** - AI insights generation
- **Amazon SageMaker** - ML model training
- **Amazon S3** - Data storage
- **Amazon DynamoDB** - User profiles
- **AWS Lambda** - Serverless functions

### Data Sources
- **Account Aggregator** - UPI transactions
- **Satellite API** - NDVI crop health
- **Weather API** - Risk assessment
- **Utility Providers** - Bill payment history

---

## 📊 Credit Score Components

| Component | Weight | Data Source |
|-----------|--------|-------------|
| Transaction Frequency | 30% | UPI via Account Aggregator |
| Agricultural Productivity | 30% | Satellite NDVI data |
| Utility Bill Hygiene | 20% | Electricity & mobile bills |
| Repayment Intent | 20% | Voice assessment (psychometric) |

**Score Range**: 300 (Poor) to 900 (Excellent)

---

## 🌍 Multilingual Support

Supported languages:
- 🇬🇧 English
- 🇮🇳 Hindi (हिन्दी)
- 🇮🇳 Marathi (मराठी)
- 🇮🇳 Telugu (తెలుగు)
- 🇮🇳 Tamil (தமிழ்)
- 🇮🇳 Kannada (ಕನ್ನಡ)

---

## 🎤 Voice Assessment Questions

The system asks 8 research-based questions:

1. **Income Stability** - Consistency of farming income
2. **Financial Discipline** - Money management (₹10,000 test)
3. **Credit History** - Past loan repayment behavior
4. **Risk Management** - Crop protection strategies
5. **Financial Literacy** - Expense tracking habits
6. **Digital Literacy** - Mobile payment comfort
7. **Future Planning** - 2-3 year farm plans
8. **Business Acumen** - Crop selection & market timing

---

## 📈 Sample Answers

See `SAMPLE_ANSWERS.md` for realistic farmer responses to all 8 questions.

---

## 🔒 Security & Privacy

- ✅ **DPDP Act 2023 Compliant** - User consent required
- ✅ **JWT Authentication** - Secure sessions
- ✅ **Role-based Access** - Farmer vs Admin
- ✅ **Data Encryption** - In transit and at rest
- ✅ **Audit Logging** - All actions tracked
- ✅ **Revocable Consent** - Users can withdraw anytime

---

## 🚀 Deployment

### Local Development
```bash
./start_integrated_system.sh
```

### Production (AWS)
See `AWS_DEPLOYMENT_GUIDE.md` for complete instructions:
- Elastic Beanstalk for backend
- CloudFront + S3 for frontend
- RDS for database
- DynamoDB for user profiles
- Bedrock for AI insights

**Estimated Cost**: $50-100/month for demo, $500-1000/month for production

---

## 📚 Documentation

- `DEMO_README.md` - Quick demo guide
- `DEMO_SHOWCASE_GUIDE.md` - Presentation script
- `LOGIN_SYSTEM_GUIDE.md` - Authentication details
- `ADMIN_PORTAL_GUIDE.md` - Admin features
- `PROFILE_PAGE_FEATURES.md` - AI insights documentation
- `AWS_DEPLOYMENT_GUIDE.md` - Production deployment
- `DATA_COLLECTION_MAPPING.md` - Data flow
- `HACKATHON_SUBMISSION.md` - Submission document

---

## 🎯 Business Impact

### Metrics
- **Target Users**: 100M+ unbanked farmers in India
- **Credit Gap**: ₹10 trillion
- **Rural Population**: 60% of India
- **Financial Inclusion**: <50% currently

### Value Proposition
- **For Farmers**: Access to formal credit, transparent scoring
- **For Banks**: Assess unbanked, reduce default risk
- **For Government**: Financial inclusion, agricultural development
- **For Economy**: Unlock rural credit market

---

## 🏆 Key Differentiators

1. ✅ **Alternative Data** - No traditional credit history needed
2. ✅ **AI-Powered** - Bedrock for personalized insights
3. ✅ **Multilingual** - 6 Indian languages supported
4. ✅ **Voice-Based** - Accessible for low-literacy users
5. ✅ **Real-Time** - Instant score calculation
6. ✅ **Compliant** - DPDP Act 2023 adherent
7. ✅ **Scalable** - AWS infrastructure

---

## 🐛 Troubleshooting

### Frontend won't start
```bash
cd gramscore-frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend won't start
```bash
cd gramscore_prototype
pip3 install -r requirements.txt
python3 api_server.py
```

### Port already in use
```bash
# Kill process on port 5001 (backend)
lsof -ti:5001 | xargs kill -9

# Kill process on port 5174 (frontend)
lsof -ti:5174 | xargs kill -9
```

### Backend offline error
- The system automatically uses mock data when backend is unavailable
- Check if backend is running: `curl http://localhost:5001/api/health`
- Restart backend: `cd gramscore_prototype && python3 api_server.py`

---

## 🤝 Contributing

This is a hackathon project. For production use:
1. Add proper authentication (OAuth, JWT)
2. Implement real AWS credentials
3. Add comprehensive testing
4. Set up CI/CD pipeline
5. Add monitoring and logging
6. Implement rate limiting
7. Add data validation

---

## 📄 License

This project was created for the AWS AI Bharat Hackathon 2024.

---

## 👥 Team

Built with ❤️ for rural India

---

## 📞 Support

For demo support:
- Check documentation files
- Review demo credentials
- Test with different farmer personas
- Try both farmer and admin flows

---

## 🎉 Acknowledgments

- AWS AI Bharat Hackathon 2024
- Grameen Bank methodology
- FICO score research
- Microfinance best practices
- Account Aggregator framework
- DPDP Act 2023 guidelines

---

**Status**: ✅ Complete and demo-ready!

**Version**: 1.0.0 (Hackathon Demo)

**Last Updated**: March 2024
