"""
Demo Data Generator for GramScore AI
Creates realistic mock data for hackathon showcase
"""

import json
from datetime import datetime, timedelta
import random

# Demo user personas
DEMO_USERS = {
    'rajesh_kumar_001': {
        'name': 'Rajesh Kumar',
        'phone': '+91-9876543210',
        'location': 'Pune, Maharashtra',
        'profile': {
            'age': 42,
            'experience_years': 20,
            'land_acres': 3.5,
            'crops': ['Rice', 'Wheat', 'Vegetables'],
            'education': 'High School',
            'family_size': 5
        },
        'gramscore': 785,
        'risk_level': 'Low',
        'loan_recommendation': {
            'approved': True,
            'amount': 200000,
            'interest_rate': 9.0,
            'tenure_months': 24,
            'emi': 9150
        },
        'data': {
            'upi_consistency': 92,
            'transaction_volume': 45000,
            'ndvi_avg': 0.72,
            'utility_payment_score': 88,
            'psychometric_score': 85,
            'weather_impact': 0.92,
            'land_size': 3.5,
            'crop_types': ['Rice', 'Wheat', 'Vegetables']
        },
        'voice_responses': {
            'q1': {
                'question': 'How do you typically plan your monthly expenses?',
                'response': 'I maintain a detailed notebook for all expenses. Every month I set aside 20% for savings and emergencies.',
                'score': 90
            },
            'q2': {
                'question': 'What would you do if you had an unexpected expense of ₹5000?',
                'response': 'I have an emergency fund of ₹15,000. If needed, I would use that first before asking family.',
                'score': 88
            },
            'q3': {
                'question': 'How do you decide when to invest in new farming equipment?',
                'response': 'I check market prices, talk to other farmers, and only buy equipment during off-season when prices are lower.',
                'score': 85
            },
            'q4': {
                'question': 'Describe your experience with digital payments like UPI.',
                'response': 'I use PhonePe daily for all payments. It\'s very convenient and I can track everything.',
                'score': 92
            },
            'q5': {
                'question': 'How confident are you about repaying a loan on time?',
                'response': 'Very confident. I have never missed a payment in 15 years of taking loans.',
                'score': 95
            }
        }
    },
    'sunita_devi_002': {
        'name': 'Sunita Devi',
        'phone': '+91-9876543211',
        'location': 'Nashik, Maharashtra',
        'profile': {
            'age': 35,
            'experience_years': 8,
            'land_acres': 1.8,
            'crops': ['Onions', 'Tomatoes'],
            'education': 'Primary School',
            'family_size': 4
        },
        'gramscore': 625,
        'risk_level': 'Medium',
        'loan_recommendation': {
            'approved': True,
            'amount': 75000,
            'interest_rate': 12.0,
            'tenure_months': 18,
            'emi': 4850,
            'conditions': ['Monthly monitoring', 'Crop insurance required']
        },
        'data': {
            'upi_consistency': 68,
            'transaction_volume': 22000,
            'ndvi_avg': 0.52,
            'utility_payment_score': 65,
            'psychometric_score': 62,
            'weather_impact': 0.78,
            'land_size': 1.8,
            'crop_types': ['Onions', 'Tomatoes']
        },
        'voice_responses': {
            'q1': {
                'question': 'How do you typically plan your monthly expenses?',
                'response': 'I try to manage expenses but sometimes it\'s difficult. I keep some money aside when I can.',
                'score': 65
            },
            'q2': {
                'question': 'What would you do if you had an unexpected expense of ₹5000?',
                'response': 'I would probably borrow from my brother or take a small loan from the local cooperative.',
                'score': 60
            },
            'q3': {
                'question': 'How do you decide when to invest in new farming equipment?',
                'response': 'When the old equipment breaks down, I buy new one. I check with 2-3 shops for prices.',
                'score': 62
            },
            'q4': {
                'question': 'Describe your experience with digital payments like UPI.',
                'response': 'I started using UPI last year. Sometimes I use it, sometimes cash. Still learning.',
                'score': 58
            },
            'q5': {
                'question': 'How confident are you about repaying a loan on time?',
                'response': 'I think I can repay on time. I will try my best to manage.',
                'score': 68
            }
        }
    },
    'ramesh_patil_003': {
        'name': 'Ramesh Patil',
        'phone': '+91-9876543212',
        'location': 'Solapur, Maharashtra',
        'profile': {
            'age': 28,
            'experience_years': 3,
            'land_acres': 0.9,
            'crops': ['Cotton'],
            'education': 'High School',
            'family_size': 3
        },
        'gramscore': 485,
        'risk_level': 'High',
        'loan_recommendation': {
            'approved': False,
            'reason': 'Insufficient credit history and low financial stability',
            'alternative': 'Government subsidy programs',
            'suggestions': [
                'Build UPI transaction history',
                'Improve crop productivity',
                'Complete financial literacy training',
                'Apply for PM-KISAN scheme'
            ]
        },
        'data': {
            'upi_consistency': 42,
            'transaction_volume': 12000,
            'ndvi_avg': 0.35,
            'utility_payment_score': 48,
            'psychometric_score': 52,
            'weather_impact': 0.65,
            'land_size': 0.9,
            'crop_types': ['Cotton']
        },
        'voice_responses': {
            'q1': {
                'question': 'How do you typically plan your monthly expenses?',
                'response': 'I don\'t really plan much. I spend as needed and hope there\'s enough left.',
                'score': 45
            },
            'q2': {
                'question': 'What would you do if you had an unexpected expense of ₹5000?',
                'response': 'I don\'t know. Maybe ask someone for help or delay the payment.',
                'score': 40
            },
            'q3': {
                'question': 'How do you decide when to invest in new farming equipment?',
                'response': 'I haven\'t bought any equipment yet. Too expensive.',
                'score': 50
            },
            'q4': {
                'question': 'Describe your experience with digital payments like UPI.',
                'response': 'I don\'t use UPI much. I prefer cash. Mobile apps are confusing.',
                'score': 35
            },
            'q5': {
                'question': 'How confident are you about repaying a loan on time?',
                'response': 'I hope I can repay. It depends on the crop yield.',
                'score': 55
            }
        }
    }
}

def get_demo_user(user_id):
    """Get demo user data by user_id"""
    return DEMO_USERS.get(user_id)

def get_all_demo_users():
    """Get all demo users"""
    return DEMO_USERS

def generate_transaction_history(user_id, days=90):
    """Generate realistic transaction history"""
    user = DEMO_USERS.get(user_id)
    if not user:
        return []
    
    consistency = user['data']['upi_consistency']
    volume = user['data']['transaction_volume']
    
    transactions = []
    current_date = datetime.now()
    
    # Merchants based on user profile
    if consistency > 80:
        merchants = {
            'business': ['Grain Buyer Co-op', 'Vegetable Market', 'Dairy Cooperative', 'Agricultural Produce Market'],
            'personal': ['Grocery Store', 'Medical Store', 'Fuel Station', 'Mobile Recharge', 'Electricity Bill']
        }
        daily_txn_prob = 0.9
    elif consistency > 60:
        merchants = {
            'business': ['Local Trader', 'Vegetable Market', 'Milk Collection'],
            'personal': ['Grocery Store', 'Medical Store', 'Mobile Recharge']
        }
        daily_txn_prob = 0.7
    else:
        merchants = {
            'business': ['Local Trader', 'Cash Sale'],
            'personal': ['Grocery Store', 'Medical Store']
        }
        daily_txn_prob = 0.4
    
    for day in range(days):
        date = current_date - timedelta(days=day)
        
        # Decide if transactions happen this day
        if random.random() < daily_txn_prob:
            # Number of transactions per day
            num_txns = random.randint(1, 4)
            
            for _ in range(num_txns):
                is_business = random.random() < 0.6
                
                if is_business:
                    merchant = random.choice(merchants['business'])
                    amount = random.uniform(500, 5000)
                    txn_type = 'credit'
                else:
                    merchant = random.choice(merchants['personal'])
                    amount = random.uniform(100, 1500)
                    txn_type = 'debit'
                
                transactions.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'merchant': merchant,
                    'amount': round(amount, 2),
                    'type': txn_type,
                    'method': 'UPI',
                    'status': 'completed'
                })
    
    return transactions

def generate_satellite_data(user_id):
    """Generate satellite NDVI data"""
    user = DEMO_USERS.get(user_id)
    if not user:
        return {}
    
    ndvi = user['data']['ndvi_avg']
    
    # Generate time series for last 12 months
    timeseries = []
    current_date = datetime.now()
    
    for month in range(12):
        date = current_date - timedelta(days=30 * month)
        
        # Seasonal variation
        month_num = date.month
        if month_num in [7, 8, 9, 10]:  # Monsoon
            seasonal_factor = 1.2
        elif month_num in [11, 12, 1, 2]:  # Winter
            seasonal_factor = 1.1
        else:  # Summer
            seasonal_factor = 0.8
        
        ndvi_value = ndvi * seasonal_factor * random.uniform(0.9, 1.1)
        ndvi_value = max(0.1, min(0.9, ndvi_value))
        
        timeseries.append({
            'date': date.strftime('%Y-%m-%d'),
            'ndvi': round(ndvi_value, 3),
            'cloud_cover': random.uniform(0, 30),
            'quality': 'good' if random.random() > 0.2 else 'moderate'
        })
    
    return {
        'coordinates': {'lat': 18.5204, 'lon': 73.8567},
        'ndvi_average': ndvi,
        'ndvi_trend': 'improving' if ndvi > 0.6 else 'stable' if ndvi > 0.4 else 'declining',
        'timeseries': timeseries,
        'land_validated': True,
        'crop_health': 'excellent' if ndvi > 0.65 else 'good' if ndvi > 0.5 else 'moderate' if ndvi > 0.35 else 'poor'
    }

def generate_utility_payments(user_id, months=12):
    """Generate utility payment history"""
    user = DEMO_USERS.get(user_id)
    if not user:
        return {}
    
    payment_score = user['data']['utility_payment_score']
    
    payments = []
    current_date = datetime.now()
    
    for month in range(months):
        bill_date = current_date - timedelta(days=30 * month)
        
        # Electricity bill
        elec_amount = random.uniform(600, 1200)
        elec_paid = random.random() < (payment_score / 100)
        elec_delay = 0 if elec_paid and random.random() > 0.3 else random.randint(1, 15)
        
        payments.append({
            'type': 'electricity',
            'bill_date': bill_date.strftime('%Y-%m-%d'),
            'due_date': (bill_date + timedelta(days=15)).strftime('%Y-%m-%d'),
            'amount': round(elec_amount, 2),
            'paid': elec_paid,
            'payment_date': (bill_date + timedelta(days=elec_delay)).strftime('%Y-%m-%d') if elec_paid else None,
            'delay_days': elec_delay if elec_paid else None
        })
        
        # Mobile bill
        mobile_amount = random.uniform(200, 500)
        mobile_paid = random.random() < (payment_score / 100)
        mobile_delay = 0 if mobile_paid and random.random() > 0.3 else random.randint(1, 10)
        
        payments.append({
            'type': 'mobile',
            'bill_date': bill_date.strftime('%Y-%m-%d'),
            'due_date': (bill_date + timedelta(days=10)).strftime('%Y-%m-%d'),
            'amount': round(mobile_amount, 2),
            'paid': mobile_paid,
            'payment_date': (bill_date + timedelta(days=mobile_delay)).strftime('%Y-%m-%d') if mobile_paid else None,
            'delay_days': mobile_delay if mobile_paid else None
        })
    
    paid_count = sum(1 for p in payments if p['paid'])
    total_count = len(payments)
    
    return {
        'payments': payments,
        'summary': {
            'total_bills': total_count,
            'paid_bills': paid_count,
            'payment_rate': round((paid_count / total_count) * 100, 1),
            'average_delay': round(sum(p['delay_days'] for p in payments if p['delay_days']) / paid_count, 1) if paid_count > 0 else 0,
            'score': payment_score
        }
    }

def generate_weather_data(user_id):
    """Generate weather risk data"""
    user = DEMO_USERS.get(user_id)
    if not user:
        return {}
    
    weather_impact = user['data']['weather_impact']
    
    # Determine risk factors based on impact score
    risk_factors = []
    if weather_impact < 0.7:
        risk_factors.extend(['drought_risk', 'extreme_weather'])
    elif weather_impact < 0.85:
        risk_factors.append('moderate_rainfall')
    
    return {
        'risk_level': 'low' if weather_impact > 0.85 else 'medium' if weather_impact > 0.7 else 'high',
        'risk_score': weather_impact,
        'risk_factors': risk_factors,
        'annual_rainfall': int(weather_impact * 1000),
        'extreme_weather_days': int((1 - weather_impact) * 30),
        'drought_risk': weather_impact < 0.7,
        'flood_risk': False
    }

def generate_ai_insights(user_id):
    """Generate AI-powered insights (mock Bedrock response)"""
    user = DEMO_USERS.get(user_id)
    if not user:
        return ""
    
    score = user['gramscore']
    risk = user['risk_level']
    
    insights = {
        'Low': f"""
Risk Assessment: {risk} Risk

Rajesh Kumar demonstrates excellent creditworthiness with a GramScore of {score}/900.

Key Strengths:
• Consistent digital payment history (92% UPI consistency)
• Strong agricultural productivity (NDVI: 0.72)
• Reliable utility payment record (88/100)
• High financial discipline and planning ability

Recommendations:
• Approved for loan amount up to ₹2,00,000
• Eligible for preferential interest rate of 9%
• Consider for premium banking services
• Suitable for agricultural equipment financing

The applicant shows strong repayment capacity and financial responsibility.
        """,
        'Medium': f"""
Risk Assessment: {risk} Risk

Sunita Devi shows moderate creditworthiness with a GramScore of {score}/900.

Key Observations:
• Moderate UPI transaction consistency (68%)
• Average agricultural productivity (NDVI: 0.52)
• Acceptable utility payment record (65/100)
• Developing financial management skills

Recommendations:
• Conditional approval for loan up to ₹75,000
• Interest rate: 12% with monthly monitoring
• Require crop insurance coverage
• Provide financial literacy training
• Review after 6 months for rate reduction

The applicant has potential but needs support and monitoring.
        """,
        'High': f"""
Risk Assessment: {risk} Risk

Ramesh Patil shows limited credit readiness with a GramScore of {score}/900.

Key Concerns:
• Low UPI transaction consistency (42%)
• Below-average agricultural productivity (NDVI: 0.35)
• Irregular utility payment pattern (48/100)
• Limited financial planning experience

Recommendations:
• Loan not recommended at this time
• Suggest government subsidy programs (PM-KISAN, PMFBY)
• Enroll in financial literacy training
• Build digital payment history over 6 months
• Focus on improving crop productivity
• Reapply after demonstrating consistent financial behavior

Alternative support options available through government schemes.
        """
    }
    
    return insights.get(risk, "")

def save_demo_data_to_file():
    """Save all demo data to JSON file"""
    demo_data = {}
    
    for user_id in DEMO_USERS.keys():
        demo_data[user_id] = {
            'profile': DEMO_USERS[user_id],
            'transactions': generate_transaction_history(user_id),
            'satellite': generate_satellite_data(user_id),
            'utilities': generate_utility_payments(user_id),
            'weather': generate_weather_data(user_id),
            'ai_insights': generate_ai_insights(user_id)
        }
    
    with open('demo_data.json', 'w') as f:
        json.dump(demo_data, f, indent=2)
    
    print("✅ Demo data saved to demo_data.json")
    return demo_data

if __name__ == '__main__':
    print("🌾 GramScore AI - Demo Data Generator")
    print("=" * 50)
    
    # Generate and save demo data
    data = save_demo_data_to_file()
    
    print("\n📊 Demo Users Created:")
    for user_id, user_data in DEMO_USERS.items():
        print(f"\n{user_data['name']} ({user_id})")
        print(f"  GramScore: {user_data['gramscore']}/900")
        print(f"  Risk Level: {user_data['risk_level']}")
        print(f"  Location: {user_data['location']}")
    
    print("\n✅ Demo data ready for showcase!")
