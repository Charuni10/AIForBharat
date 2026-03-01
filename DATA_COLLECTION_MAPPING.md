# GramScore AI - Data Collection Mapping

## Overview
This document maps the data collected from users to the backend ML model features and scoring components.

---

## Voice Assessment Questions

The voice assessment collects psychometric data through 5 key questions across multiple categories:

### 1. Financial Discipline
**Question (EN):** "How do you typically plan your monthly expenses?"
**Question (HI):** "आप आमतौर पर अपने मासिक खर्चों की योजना कैसे बनाते हैं?"
**Question (MR):** "तुम्ही सामान्यतः तुमच्या मासिक खर्चाची योजना कशी करता?"

**Expected Keywords:** budget, plan, save, track, record
**Backend Mapping:** `psychometric_score` (30% weight in psychometric assessment)
**Purpose:** Assesses user's ability to manage finances systematically

### 2. Risk Awareness
**Question (EN):** "What would you do if you had an unexpected expense of ₹5000?"
**Question (HI):** "यदि आपको ₹5000 का अप्रत्याशित खर्च करना पड़े तो आप क्या करेंगे?"
**Question (MR):** "जर तुम्हाला ₹5000 चा अनपेक्षित खर्च करावा लागला तर तुम्ही काय कराल?"

**Expected Keywords:** borrow, save, family, loan, emergency
**Backend Mapping:** `psychometric_score` (25% weight in psychometric assessment)
**Purpose:** Evaluates user's preparedness for financial emergencies

### 3. Planning Ability
**Question (EN):** "How do you decide when to invest in new farming equipment?"
**Question (HI):** "आप नए कृषि उपकरण में निवेश करने का निर्णय कैसे लेते हैं?"
**Question (MR):** "नवीन शेती उपकरणांमध्ये गुंतवणूक करण्याचा निर्णय तुम्ही कसा घेता?"

**Expected Keywords:** profit, need, season, money, benefit
**Backend Mapping:** `psychometric_score` (20% weight in psychometric assessment)
**Purpose:** Measures strategic thinking and investment decision-making

### 4. Digital Literacy
**Question (EN):** "Describe your experience with digital payments like UPI."
**Question (HI):** "UPI जैसे डिजिटल भुगतान के साथ आपका अनुभव कैसा है?"
**Question (MR):** "UPI सारख्या डिजिटल पेमेंटचा तुमचा अनुभव कसा आहे?"

**Expected Keywords:** easy, use, phone, payment, app
**Backend Mapping:** `digital_literacy_score` (derived feature)
**Purpose:** Assesses comfort with digital financial tools

### 5. Confidence Level
**Question (EN):** "How confident are you about repaying a loan on time?"
**Question (HI):** "समय पर लोन चुकाने के बारे में आप कितने आत्मविश्वास से भरे हैं?"
**Question (MR):** "वेळेवर लोन परत करण्याबद्दल तुम्ही किती आत्मविश्वासाने भरलेले आहात?"

**Expected Keywords:** confident, sure, definitely, always, never
**Backend Mapping:** `psychometric_score` (10% weight in psychometric assessment)
**Purpose:** Gauges repayment intent and self-confidence

---

## Complete Data Collection Flow

### 1. Consent Form Data
**Collected From:** ConsentForm.jsx
**Data Points:**
- User consent for UPI transactions
- User consent for satellite data
- User consent for utility payments
- Consent timestamp
- User ID

**Backend Mapping:**
```javascript
{
  user_id: string,
  data_types: ['transactions', 'satellite', 'utilities'],
  consent_given: boolean,
  timestamp: ISO datetime
}
```

### 2. Voice Assessment Data
**Collected From:** VoiceAssessment.jsx
**Data Points:**
- 5 question responses (text or voice)
- Response category (financial_discipline, risk_awareness, etc.)
- Expected keywords for each response
- Language preference
- Input mode (chat/voice)

**Backend Mapping:**
```javascript
{
  responses: {
    q1: {
      question: string,
      response: string,
      category: 'financial_discipline',
      type: 'text' | 'voice',
      expected_keywords: string[]
    },
    // ... q2-q5
  },
  language: 'en' | 'hi' | 'mr' | 'te' | 'ta' | 'kn'
}
```

**Backend Processing:**
- Keyword matching score (40% weight)
- Response length score (30% weight)
- Sentiment analysis score (30% weight)
- Combined into `psychometric_score` (0-100)

### 3. Transaction Data (Account Aggregator)
**Collected From:** Backend data sources
**Data Points:**
- UPI transaction history (90 days)
- Transaction frequency
- Business inflow vs personal outflow ratio
- Average transaction amount
- Merchant categories

**Backend Mapping:**
```python
{
  'upi_consistency': float (0-100),
  'transaction_volume': float (monthly volume),
  'transaction_volume_normalized': float (log-transformed),
  'seasonal_consistency': float (0-100)
}
```

**ML Model Features:**
- `upi_consistency` - 30% weight in final score
- `transaction_volume_normalized` - 10% weight

### 4. Satellite Data (NDVI)
**Collected From:** Backend satellite service
**Data Points:**
- NDVI time series (365 days)
- Average NDVI value
- Seasonal variations
- Cloud cover percentage
- Land validation status

**Backend Mapping:**
```python
{
  'ndvi_avg': float (0-1),
  'land_size_normalized': float (log-transformed),
  'crop_diversity_score': int (1-5)
}
```

**ML Model Features:**
- `ndvi_avg` - 30% weight in final score
- Indicates agricultural productivity

### 5. Weather Data
**Collected From:** Backend weather service
**Data Points:**
- Historical weather (365 days)
- Rainfall totals
- Temperature extremes
- Risk factors (drought, heat stress)
- Weather impact score

**Backend Mapping:**
```python
{
  'weather_impact': float (0.2-1.2),
  'risk_level': 'low' | 'medium' | 'high'
}
```

**ML Model Features:**
- `weather_impact` - 5% weight in final score
- Adjusts score based on environmental risks

### 6. Utility Payment Data
**Collected From:** Backend utility service
**Data Points:**
- Electricity bill payment history (12 months)
- Mobile bill payment history (12 months)
- Payment timeliness
- Payment delay days
- Unpaid bills count

**Backend Mapping:**
```python
{
  'utility_payment_score': float (0-100),
  'payment_rate': float (0-1),
  'average_delay_days': float
}
```

**ML Model Features:**
- `utility_payment_score` - 20% weight in final score

---

## ML Model Feature Vector

The complete feature vector sent to the ML model:

```python
feature_vector = [
    upi_consistency,              # 0-100
    transaction_volume_normalized, # log(volume)
    ndvi_avg,                     # 0-1
    utility_payment_score,        # 0-100
    psychometric_score,           # 0-100 (from voice assessment)
    weather_impact,               # 0.2-1.2
    land_size_normalized,         # log(land_size + 1)
    crop_diversity_score,         # 1-5
    seasonal_consistency,         # 0-100
    digital_literacy_score        # 0-100
]
```

---

## GramScore Calculation

### Score Components (Weighted Average)
1. **Transaction Frequency (30%)** - From UPI consistency
2. **Agricultural Productivity (30%)** - From NDVI data
3. **Utility Bill Hygiene (20%)** - From payment history
4. **Repayment Intent (20%)** - From psychometric assessment

### Final Score Formula
```
base_score = (upi_consistency * 0.30) + 
             (ndvi_avg * 100 * 0.30) + 
             (utility_payment_score * 0.20) + 
             (psychometric_score * 0.20)

adjustments = weather_impact * volume_adjustment * land_adjustment

final_score = 300 + (base_score * adjustments * 6)
final_score = clip(final_score, 300, 900)
```

### Score Ranges
- **750-900**: Excellent - Low-interest micro-loan approved
- **650-749**: Good - Standard loan terms
- **550-649**: Fair - Conditional approval with monitoring
- **300-549**: Poor - Government subsidy recommended

---

## API Endpoints Used

### Frontend → Backend
1. `POST /api/consent` - Submit user consent
2. `POST /api/voice/assess` - Submit voice assessment responses
3. `POST /api/data/collect` - Trigger data collection from all sources
4. `POST /api/score/calculate` - Calculate final GramScore
5. `GET /api/score/history/:userId` - Get score history

### Backend → External Services
1. Account Aggregator API - Transaction data
2. Sentinel-2 / Google Earth Engine - Satellite NDVI data
3. IMD / OpenWeather API - Weather data
4. Utility Provider APIs - Bill payment history
5. AWS Bedrock - AI insights and sentiment analysis

---

## Data Privacy & Security

### Compliance
- DPDP Act 2023 compliant
- User consent required for all data access
- 90-day consent validity period
- User can revoke consent anytime

### Security Measures
- Bank-grade encryption for data transmission
- JWT authentication for API access
- Secure token management
- No PII stored in logs
- Data anonymization for ML training

---

## Language Support

All questions available in 6 languages:
- English (en)
- Hindi (hi)
- Marathi (mr)
- Telugu (te)
- Tamil (ta)
- Kannada (kn)

Backend processes responses in any language using multilingual NLP models.

---

## Testing the Complete Flow

1. **Start Backend:** `python3 gramscore_prototype/api_server.py`
2. **Start Frontend:** `cd gramscore-frontend && npm run dev`
3. **Navigate to:** http://localhost:5173
4. **Complete Consent Form** → Approve all data sources
5. **Complete Voice Assessment** → Answer all 5 questions (chat or voice mode)
6. **View Dashboard** → See calculated GramScore with breakdown

---

## Summary

The system collects comprehensive data across 5 dimensions:
1. **Financial Behavior** - UPI transactions, utility payments
2. **Agricultural Assets** - Satellite NDVI, land validation
3. **Environmental Risk** - Weather patterns, climate impact
4. **Psychometric Profile** - Voice assessment responses
5. **Digital Literacy** - UPI usage, digital payment comfort

All data is processed through ML models to generate a holistic credit score (300-900) that reflects the true creditworthiness of rural farmers beyond traditional credit history.
