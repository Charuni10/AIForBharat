"""
Data Sources Integration for GramScore AI
Handles Account Aggregator, Satellite Data, and other external data sources
"""

import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AccountAggregatorService:
    """Integration with Account Aggregator for UPI transaction data"""
    
    def __init__(self, base_url: str = "https://api.sahamati.org.in/sandbox"):
        self.base_url = base_url
        self.api_key = "demo_api_key"  # In production, use secure key management
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        })
    
    def get_consent_token(self, user_id: str, data_types: List[str]) -> Dict:
        """Get user consent for data access"""
        consent_request = {
            "user_id": user_id,
            "data_types": data_types,
            "purpose": "credit_assessment",
            "validity_period": 90,  # days
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Mock consent response for demo
            return {
                "consent_token": f"consent_{user_id}_{int(time.time())}",
                "status": "approved",
                "expires_at": (datetime.now() + timedelta(days=90)).isoformat(),
                "data_types_approved": data_types
            }
        except Exception as e:
            logger.error(f"Consent request failed: {str(e)}")
            return {"status": "failed", "error": str(e)}
    
    def fetch_transaction_data(self, consent_token: str, date_range: Tuple[str, str]) -> pd.DataFrame:
        """Fetch UPI transaction data using consent token"""
        start_date, end_date = date_range
        
        try:
            # Mock API call - in production, this would call actual AA API
            logger.info(f"Fetching transaction data from {start_date} to {end_date}")
            
            # Generate synthetic transaction data
            transactions = self._generate_synthetic_transactions(start_date, end_date)
            
            return pd.DataFrame(transactions)
            
        except Exception as e:
            logger.error(f"Transaction data fetch failed: {str(e)}")
            return pd.DataFrame()
    
    def _generate_synthetic_transactions(self, start_date: str, end_date: str) -> List[Dict]:
        """Generate synthetic UPI transaction data for demo"""
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        transactions = []
        current_date = start
        
        # Transaction patterns
        merchants = {
            'business_inflow': [
                'Grain Buyer Co-op', 'Vegetable Market', 'Dairy Cooperative', 
                'Local Trader', 'Agricultural Produce Market', 'Milk Collection Center'
            ],
            'personal_outflow': [
                'Grocery Store', 'Medical Store', 'Fuel Station', 'Utility Payment',
                'School Fees', 'Insurance Premium', 'Mobile Recharge'
            ]
        }
        
        while current_date <= end:
            # Generate 1-5 transactions per day
            num_transactions = np.random.poisson(2) + 1
            
            for _ in range(num_transactions):
                # 60% business inflow, 40% personal outflow
                is_business = np.random.random() < 0.6
                
                if is_business:
                    category = 'business_inflow'
                    amount = np.random.lognormal(mean=7, sigma=0.8)  # Higher amounts
                    merchant = np.random.choice(merchants['business_inflow'])
                else:
                    category = 'personal_outflow'
                    amount = np.random.lognormal(mean=5.5, sigma=0.7)  # Lower amounts
                    merchant = np.random.choice(merchants['personal_outflow'])
                
                # Add transaction time
                transaction_time = current_date + timedelta(
                    hours=np.random.randint(6, 22),
                    minutes=np.random.randint(0, 60)
                )
                
                transactions.append({
                    'transaction_id': f'TXN_{len(transactions):06d}',
                    'timestamp': transaction_time.isoformat(),
                    'amount': round(amount, 2),
                    'type': 'credit' if is_business else 'debit',
                    'category': category,
                    'merchant_name': merchant,
                    'payment_method': 'UPI',
                    'status': 'completed',
                    'description': f'Payment to {merchant}'
                })
            
            current_date += timedelta(days=1)
        
        return transactions
    
    def analyze_transaction_patterns(self, transactions_df: pd.DataFrame) -> Dict:
        """Analyze transaction patterns for credit scoring"""
        if transactions_df.empty:
            return {'consistency_score': 0, 'volume_score': 0, 'pattern_analysis': {}}
        
        # Convert timestamp to datetime
        transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'])
        transactions_df['date'] = transactions_df['timestamp'].dt.date
        
        # Calculate consistency metrics
        daily_transactions = transactions_df.groupby('date').size()
        consistency_score = min(100, (daily_transactions > 0).sum() / len(daily_transactions) * 100)
        
        # Calculate volume metrics
        total_volume = transactions_df['amount'].sum()
        avg_daily_volume = total_volume / len(daily_transactions)
        volume_score = min(100, np.log(avg_daily_volume / 100) * 20 + 50)
        volume_score = max(0, volume_score)
        
        # Business vs personal ratio
        business_transactions = transactions_df[transactions_df['category'] == 'business_inflow']
        business_ratio = len(business_transactions) / len(transactions_df) if len(transactions_df) > 0 else 0
        
        # Pattern analysis
        pattern_analysis = {
            'total_transactions': len(transactions_df),
            'business_inflow_ratio': business_ratio,
            'avg_transaction_amount': transactions_df['amount'].mean(),
            'transaction_frequency_per_day': len(transactions_df) / len(daily_transactions),
            'top_merchants': transactions_df['merchant_name'].value_counts().head(5).to_dict()
        }
        
        return {
            'consistency_score': consistency_score,
            'volume_score': volume_score,
            'pattern_analysis': pattern_analysis
        }

class SatelliteDataService:
    """Integration with satellite data providers for agricultural assessment"""
    
    def __init__(self):
        self.sentinel_api_url = "https://scihub.copernicus.eu/dhus/search"
        self.google_earth_engine_url = "https://earthengine.googleapis.com/v1alpha"
        
    def get_ndvi_data(self, coordinates: Dict, date_range: Tuple[str, str]) -> Dict:
        """Get NDVI data for given coordinates and date range"""
        lat, lon = coordinates['lat'], coordinates['lon']
        start_date, end_date = date_range
        
        try:
            # Mock satellite data - in production, integrate with actual APIs
            logger.info(f"Fetching NDVI data for coordinates ({lat}, {lon})")
            
            # Generate realistic NDVI time series
            ndvi_data = self._generate_ndvi_timeseries(lat, lon, start_date, end_date)
            
            return {
                'coordinates': coordinates,
                'date_range': date_range,
                'ndvi_timeseries': ndvi_data,
                'average_ndvi': np.mean([d['ndvi'] for d in ndvi_data]),
                'data_source': 'Sentinel-2',
                'cloud_cover_avg': np.mean([d['cloud_cover'] for d in ndvi_data])
            }
            
        except Exception as e:
            logger.error(f"NDVI data fetch failed: {str(e)}")
            return {'error': str(e)}
    
    def _generate_ndvi_timeseries(self, lat: float, lon: float, start_date: str, end_date: str) -> List[Dict]:
        """Generate synthetic NDVI time series data"""
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        # Base NDVI based on location (rough approximation for India)
        base_ndvi = 0.4 + (lat - 15) * 0.02  # Higher NDVI for northern regions
        base_ndvi = np.clip(base_ndvi, 0.2, 0.8)
        
        ndvi_data = []
        current_date = start
        
        while current_date <= end:
            # Seasonal variation (higher NDVI during monsoon/post-monsoon)
            month = current_date.month
            if month in [7, 8, 9, 10]:  # Monsoon and post-monsoon
                seasonal_factor = 1.2
            elif month in [11, 12, 1, 2]:  # Winter crops
                seasonal_factor = 1.1
            else:  # Summer
                seasonal_factor = 0.8
            
            # Add random variation
            ndvi_value = base_ndvi * seasonal_factor * np.random.uniform(0.8, 1.2)
            ndvi_value = np.clip(ndvi_value, 0.1, 0.9)
            
            # Cloud cover affects data quality
            cloud_cover = np.random.uniform(0, 50)
            
            ndvi_data.append({
                'date': current_date.isoformat(),
                'ndvi': round(ndvi_value, 3),
                'cloud_cover': round(cloud_cover, 1),
                'data_quality': 'good' if cloud_cover < 20 else 'moderate'
            })
            
            # Move to next observation (every 5 days for Sentinel-2)
            current_date += timedelta(days=5)
        
        return ndvi_data
    
    def validate_land_coordinates(self, coordinates: Dict, land_record_number: str = None) -> Dict:
        """Validate if coordinates correspond to agricultural land"""
        lat, lon = coordinates['lat'], coordinates['lon']
        
        # Mock land validation - in production, integrate with land records API
        logger.info(f"Validating land coordinates ({lat}, {lon})")
        
        # Simple validation based on coordinates (rough approximation)
        is_agricultural = True
        confidence = 0.85
        
        # Check if coordinates are within India
        if not (6.0 <= lat <= 37.0 and 68.0 <= lon <= 98.0):
            is_agricultural = False
            confidence = 0.0
        
        return {
            'coordinates': coordinates,
            'is_agricultural_land': is_agricultural,
            'confidence': confidence,
            'land_record_number': land_record_number,
            'validation_source': 'Bhuvan NOEDA (Mock)',
            'land_type': 'agricultural' if is_agricultural else 'non-agricultural'
        }

class WeatherDataService:
    """Integration with weather data providers for environmental risk assessment"""
    
    def __init__(self, api_key: str = "demo_api_key"):
        self.api_key = api_key
        self.openweather_url = "https://api.openweathermap.org/data/2.5"
        self.imd_url = "https://imdpune.gov.in/Clim_Pred_LRF_New/Grided_Data_Download.html"
    
    def get_weather_history(self, coordinates: Dict, date_range: Tuple[str, str]) -> Dict:
        """Get historical weather data for risk assessment"""
        lat, lon = coordinates['lat'], coordinates['lon']
        start_date, end_date = date_range
        
        try:
            # Mock weather data - in production, integrate with IMD or OpenWeather APIs
            logger.info(f"Fetching weather data for coordinates ({lat}, {lon})")
            
            weather_data = self._generate_weather_data(lat, lon, start_date, end_date)
            
            return {
                'coordinates': coordinates,
                'date_range': date_range,
                'weather_data': weather_data,
                'risk_assessment': self._assess_weather_risk(weather_data),
                'data_source': 'IMD Pune (Mock)'
            }
            
        except Exception as e:
            logger.error(f"Weather data fetch failed: {str(e)}")
            return {'error': str(e)}
    
    def _generate_weather_data(self, lat: float, lon: float, start_date: str, end_date: str) -> List[Dict]:
        """Generate synthetic weather data"""
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        weather_data = []
        current_date = start
        
        while current_date <= end:
            month = current_date.month
            
            # Seasonal temperature patterns for India
            if month in [3, 4, 5]:  # Summer
                temp_base = 35
                rainfall_prob = 0.1
            elif month in [6, 7, 8, 9]:  # Monsoon
                temp_base = 28
                rainfall_prob = 0.7
            elif month in [10, 11]:  # Post-monsoon
                temp_base = 25
                rainfall_prob = 0.3
            else:  # Winter
                temp_base = 20
                rainfall_prob = 0.1
            
            # Generate daily weather
            temperature = temp_base + np.random.normal(0, 5)
            humidity = np.random.uniform(40, 90)
            
            # Rainfall
            if np.random.random() < rainfall_prob:
                rainfall = np.random.exponential(10)  # mm
            else:
                rainfall = 0
            
            weather_data.append({
                'date': current_date.isoformat(),
                'temperature_max': round(temperature + np.random.uniform(0, 5), 1),
                'temperature_min': round(temperature - np.random.uniform(5, 10), 1),
                'humidity': round(humidity, 1),
                'rainfall': round(rainfall, 1),
                'wind_speed': round(np.random.uniform(5, 25), 1)
            })
            
            current_date += timedelta(days=1)
        
        return weather_data
    
    def _assess_weather_risk(self, weather_data: List[Dict]) -> Dict:
        """Assess weather-related agricultural risk"""
        if not weather_data:
            return {'risk_level': 'unknown', 'risk_score': 0.5}
        
        # Calculate risk factors
        total_rainfall = sum(d['rainfall'] for d in weather_data)
        avg_temp = np.mean([d['temperature_max'] for d in weather_data])
        extreme_temp_days = sum(1 for d in weather_data if d['temperature_max'] > 40 or d['temperature_max'] < 10)
        
        # Risk assessment logic
        risk_factors = []
        risk_score = 1.0  # Start with no risk
        
        # Drought risk
        if total_rainfall < 500:  # mm per year
            risk_factors.append('drought_risk')
            risk_score *= 0.7
        
        # Heat stress risk
        if avg_temp > 35:
            risk_factors.append('heat_stress')
            risk_score *= 0.8
        
        # Extreme weather risk
        if extreme_temp_days > len(weather_data) * 0.1:
            risk_factors.append('extreme_weather')
            risk_score *= 0.9
        
        # Determine risk level
        if risk_score > 0.8:
            risk_level = 'low'
        elif risk_score > 0.6:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'total_rainfall': total_rainfall,
            'average_temperature': avg_temp,
            'extreme_weather_days': extreme_temp_days
        }

class UtilityPaymentService:
    """Integration with utility payment data for bill payment history"""
    
    def __init__(self):
        self.electricity_boards = {
            'Maharashtra': 'MSEDCL',
            'Karnataka': 'BESCOM',
            'Tamil Nadu': 'TNEB',
            'Gujarat': 'GUVNL'
        }
    
    def get_utility_payment_history(self, user_id: str, utility_types: List[str], months: int = 12) -> Dict:
        """Get utility payment history for credit assessment"""
        try:
            logger.info(f"Fetching utility payment history for user {user_id}")
            
            payment_history = self._generate_utility_payments(user_id, utility_types, months)
            payment_score = self._calculate_payment_score(payment_history)
            
            return {
                'user_id': user_id,
                'payment_history': payment_history,
                'payment_score': payment_score,
                'analysis_period_months': months
            }
            
        except Exception as e:
            logger.error(f"Utility payment data fetch failed: {str(e)}")
            return {'error': str(e)}
    
    def _generate_utility_payments(self, user_id: str, utility_types: List[str], months: int) -> List[Dict]:
        """Generate synthetic utility payment data"""
        payments = []
        
        for month_offset in range(months):
            payment_date = datetime.now() - timedelta(days=30 * month_offset)
            
            for utility_type in utility_types:
                # Payment probability (some users miss payments)
                payment_made = np.random.random() > 0.15  # 85% payment rate
                
                if utility_type == 'electricity':
                    base_amount = np.random.normal(800, 200)
                elif utility_type == 'mobile':
                    base_amount = np.random.normal(300, 100)
                elif utility_type == 'gas':
                    base_amount = np.random.normal(600, 150)
                else:
                    base_amount = np.random.normal(500, 150)
                
                amount = max(100, base_amount)
                
                # Payment delay (0-30 days)
                if payment_made:
                    delay_days = max(0, np.random.poisson(3))
                    actual_payment_date = payment_date + timedelta(days=delay_days)
                    status = 'paid'
                else:
                    delay_days = None
                    actual_payment_date = None
                    status = 'unpaid'
                
                payments.append({
                    'utility_type': utility_type,
                    'bill_date': payment_date.isoformat(),
                    'due_date': (payment_date + timedelta(days=15)).isoformat(),
                    'payment_date': actual_payment_date.isoformat() if actual_payment_date else None,
                    'amount': round(amount, 2),
                    'status': status,
                    'delay_days': delay_days
                })
        
        return payments
    
    def _calculate_payment_score(self, payment_history: List[Dict]) -> Dict:
        """Calculate utility payment score for credit assessment"""
        if not payment_history:
            return {'score': 0, 'analysis': {}}
        
        paid_bills = [p for p in payment_history if p['status'] == 'paid']
        total_bills = len(payment_history)
        
        # Payment rate
        payment_rate = len(paid_bills) / total_bills if total_bills > 0 else 0
        
        # Average delay
        delays = [p['delay_days'] for p in paid_bills if p['delay_days'] is not None]
        avg_delay = np.mean(delays) if delays else 0
        
        # Score calculation (0-100)
        base_score = payment_rate * 100
        delay_penalty = min(30, avg_delay * 2)  # Max 30 points penalty
        final_score = max(0, base_score - delay_penalty)
        
        return {
            'score': round(final_score, 1),
            'analysis': {
                'payment_rate': round(payment_rate * 100, 1),
                'average_delay_days': round(avg_delay, 1),
                'total_bills': total_bills,
                'paid_bills': len(paid_bills),
                'unpaid_bills': total_bills - len(paid_bills)
            }
        }

class DataSourceOrchestrator:
    """Main orchestrator for all data sources"""
    
    def __init__(self):
        self.account_aggregator = AccountAggregatorService()
        self.satellite_service = SatelliteDataService()
        self.weather_service = WeatherDataService()
        self.utility_service = UtilityPaymentService()
    
    def collect_all_data(self, user_profile: Dict) -> Dict:
        """Collect data from all sources for a user"""
        user_id = user_profile['user_id']
        coordinates = user_profile.get('location', {}).get('coordinates', {'lat': 18.5, 'lon': 73.8})
        
        # Date range for data collection (last 12 months)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        date_range = (start_date.isoformat(), end_date.isoformat())
        
        collected_data = {}
        
        try:
            # Get consent for data access
            consent = self.account_aggregator.get_consent_token(
                user_id, ['transactions', 'satellite', 'weather', 'utilities']
            )
            
            if consent['status'] == 'approved':
                # Collect transaction data
                logger.info("Collecting transaction data...")
                transactions_df = self.account_aggregator.fetch_transaction_data(
                    consent['consent_token'], date_range
                )
                transaction_analysis = self.account_aggregator.analyze_transaction_patterns(transactions_df)
                collected_data['transactions'] = {
                    'raw_data': transactions_df.to_dict('records') if not transactions_df.empty else [],
                    'analysis': transaction_analysis
                }
                
                # Collect satellite data
                logger.info("Collecting satellite data...")
                ndvi_data = self.satellite_service.get_ndvi_data(coordinates, date_range)
                land_validation = self.satellite_service.validate_land_coordinates(coordinates)
                collected_data['satellite'] = {
                    'ndvi_data': ndvi_data,
                    'land_validation': land_validation
                }
                
                # Collect weather data
                logger.info("Collecting weather data...")
                weather_data = self.weather_service.get_weather_history(coordinates, date_range)
                collected_data['weather'] = weather_data
                
                # Collect utility payment data
                logger.info("Collecting utility payment data...")
                utility_data = self.utility_service.get_utility_payment_history(
                    user_id, ['electricity', 'mobile'], 12
                )
                collected_data['utilities'] = utility_data
                
                collected_data['consent'] = consent
                collected_data['collection_timestamp'] = datetime.now().isoformat()
                collected_data['status'] = 'success'
                
            else:
                collected_data['status'] = 'consent_failed'
                collected_data['error'] = consent.get('error', 'Consent not approved')
        
        except Exception as e:
            logger.error(f"Data collection failed: {str(e)}")
            collected_data['status'] = 'failed'
            collected_data['error'] = str(e)
        
        return collected_data
    
    def prepare_features_for_ml(self, collected_data: Dict) -> Dict:
        """Prepare features from collected data for ML model"""
        features = {}
        
        try:
            # Transaction features
            if 'transactions' in collected_data and collected_data['transactions']['analysis']:
                trans_analysis = collected_data['transactions']['analysis']
                features['upi_consistency'] = trans_analysis.get('consistency_score', 0)
                features['transaction_volume'] = trans_analysis['pattern_analysis'].get('avg_transaction_amount', 0) * 30  # Monthly volume
            
            # Satellite features
            if 'satellite' in collected_data and 'ndvi_data' in collected_data['satellite']:
                ndvi_data = collected_data['satellite']['ndvi_data']
                features['ndvi_avg'] = ndvi_data.get('average_ndvi', 0)
            
            # Weather features
            if 'weather' in collected_data and 'risk_assessment' in collected_data['weather']:
                weather_risk = collected_data['weather']['risk_assessment']
                features['weather_impact'] = weather_risk.get('risk_score', 0.8)
            
            # Utility features
            if 'utilities' in collected_data and 'payment_score' in collected_data['utilities']:
                utility_score = collected_data['utilities']['payment_score']
                features['utility_payment_score'] = utility_score.get('score', 50)
            
            # Default psychometric score (would come from voice assessment)
            features['psychometric_score'] = 65  # Default value
            
            # Additional derived features
            features['land_size'] = 2.0  # Default land size
            features['crop_types'] = ['Mixed Crops']
            
        except Exception as e:
            logger.error(f"Feature preparation failed: {str(e)}")
            # Return default features
            features = {
                'upi_consistency': 50,
                'transaction_volume': 10000,
                'ndvi_avg': 0.4,
                'weather_impact': 0.8,
                'utility_payment_score': 60,
                'psychometric_score': 65,
                'land_size': 1.0,
                'crop_types': []
            }
        
        return features