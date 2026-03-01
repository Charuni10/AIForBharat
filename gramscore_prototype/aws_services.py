"""
AWS Services Integration for GramScore AI
Handles Bedrock, SageMaker, and other AWS service integrations
"""

import boto3
import json
import numpy as np
from botocore.exceptions import ClientError
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BedrockService:
    """AWS Bedrock integration for AI-powered insights"""
    
    def __init__(self, region_name: str = 'ap-south-1'):
        self.region_name = region_name
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Bedrock client"""
        try:
            self.client = boto3.client('bedrock-runtime', region_name=self.region_name)
            logger.info(f"Bedrock client initialized for region: {self.region_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {str(e)}")
            self.client = None
    
    def generate_credit_insights(self, user_data: Dict) -> Dict:
        """Generate credit insights using Bedrock"""
        if not self.client:
            return self._mock_bedrock_response(user_data)
        
        prompt = self._create_credit_analysis_prompt(user_data)
        
        try:
            response = self.client.invoke_model(
                modelId="amazon.titan-text-express-v1",
                body=json.dumps({
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 500,
                        "temperature": 0.3,
                        "topP": 0.9
                    }
                })
            )
            
            result = json.loads(response['body'].read())
            return {
                "insights": result['results'][0]['outputText'],
                "confidence": 0.85,
                "source": "AWS Bedrock"
            }
            
        except ClientError as e:
            logger.error(f"Bedrock API error: {str(e)}")
            return self._mock_bedrock_response(user_data)
    
    def _create_credit_analysis_prompt(self, user_data: Dict) -> str:
        """Create prompt for credit analysis"""
        return f"""
        Analyze the creditworthiness of a rural farmer with the following profile:
        
        - UPI Transaction Consistency: {user_data.get('upi_consistency', 0)}%
        - Agricultural Productivity (NDVI): {user_data.get('ndvi_avg', 0):.2f}
        - Utility Payment Score: {user_data.get('utility_payment_score', 0)}/100
        - Psychometric Score: {user_data.get('psychometric_score', 0)}/100
        - Land Size: {user_data.get('land_size', 0)} acres
        - Crop Types: {', '.join(user_data.get('crop_types', []))}
        
        Provide:
        1. Risk assessment (Low/Medium/High)
        2. Key strengths and weaknesses
        3. Specific recommendations for improvement
        4. Suitable loan products
        
        Keep the response concise and actionable for rural users.
        """
    
    def _mock_bedrock_response(self, user_data: Dict) -> Dict:
        """Mock response when Bedrock is unavailable"""
        score = user_data.get('upi_consistency', 50)
        
        if score >= 80:
            risk = "Low Risk"
            insights = "Strong digital payment history and good agricultural productivity indicate reliable repayment capacity."
        elif score >= 60:
            risk = "Medium Risk"
            insights = "Moderate transaction consistency. Consider improving utility payment regularity."
        else:
            risk = "High Risk"
            insights = "Limited transaction history. Focus on building digital payment habits and improving crop productivity."
        
        return {
            "insights": f"Risk Assessment: {risk}\n\n{insights}",
            "confidence": 0.75,
            "source": "Mock Response"
        }

class SageMakerService:
    """AWS SageMaker integration for ML model inference"""
    
    def __init__(self, region_name: str = 'ap-south-1'):
        self.region_name = region_name
        self.client = None
        self.endpoint_name = "gramscore-xgboost-endpoint"  # Your deployed endpoint
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize SageMaker client"""
        try:
            self.client = boto3.client('sagemaker-runtime', region_name=self.region_name)
            logger.info(f"SageMaker client initialized for region: {self.region_name}")
        except Exception as e:
            logger.error(f"Failed to initialize SageMaker client: {str(e)}")
            self.client = None
    
    def predict_credit_score(self, features: List[float]) -> Dict:
        """Predict credit score using SageMaker endpoint"""
        if not self.client:
            return self._mock_sagemaker_prediction(features)
        
        try:
            # Prepare input data for XGBoost model
            input_data = ','.join(map(str, features))
            
            response = self.client.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='text/csv',
                Body=input_data
            )
            
            result = json.loads(response['Body'].read().decode())
            predicted_score = int(result[0])  # Assuming single prediction
            
            return {
                "predicted_score": max(300, min(900, predicted_score)),
                "confidence": 0.92,
                "model_version": "v1.0",
                "feature_importance": self._calculate_feature_importance(features),
                "source": "AWS SageMaker"
            }
            
        except ClientError as e:
            logger.error(f"SageMaker inference error: {str(e)}")
            return self._mock_sagemaker_prediction(features)
    
    def _calculate_feature_importance(self, features: List[float]) -> Dict:
        """Calculate feature importance (mock implementation)"""
        feature_names = [
            'transaction_frequency',
            'agricultural_productivity', 
            'utility_payments',
            'psychometric_score'
        ]
        
        # Mock SHAP values
        importance = {
            feature_names[i]: abs(features[i] - 50) / 100 
            for i in range(min(len(features), len(feature_names)))
        }
        
        # Normalize to sum to 1
        total = sum(importance.values())
        if total > 0:
            importance = {k: v/total for k, v in importance.items()}
        
        return importance
    
    def _mock_sagemaker_prediction(self, features: List[float]) -> Dict:
        """Mock prediction when SageMaker is unavailable"""
        # Simple weighted average for mock prediction
        weights = [0.30, 0.30, 0.20, 0.20]
        weighted_score = sum(f * w for f, w in zip(features, weights))
        predicted_score = int(300 + (weighted_score * 6))
        
        return {
            "predicted_score": max(300, min(900, predicted_score)),
            "confidence": 0.78,
            "model_version": "mock",
            "feature_importance": {
                'transaction_frequency': 0.30,
                'agricultural_productivity': 0.30,
                'utility_payments': 0.20,
                'psychometric_score': 0.20
            },
            "source": "Mock Prediction"
        }

class S3DataService:
    """AWS S3 integration for data storage and retrieval"""
    
    def __init__(self, region_name: str = 'ap-south-1', bucket_name: str = 'gramscore-data-lake'):
        self.region_name = region_name
        self.bucket_name = bucket_name
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize S3 client"""
        try:
            self.client = boto3.client('s3', region_name=self.region_name)
            logger.info(f"S3 client initialized for region: {self.region_name}")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {str(e)}")
            self.client = None
    
    def store_user_data(self, user_id: str, data: Dict) -> bool:
        """Store user data in S3"""
        if not self.client:
            logger.warning("S3 client not available, data not stored")
            return False
        
        try:
            key = f"user-data/{user_id}/profile.json"
            
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=json.dumps(data, indent=2),
                ContentType='application/json',
                ServerSideEncryption='AES256'
            )
            
            logger.info(f"User data stored successfully: {key}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to store user data: {str(e)}")
            return False
    
    def retrieve_satellite_data(self, coordinates: Dict) -> Optional[Dict]:
        """Retrieve satellite data from S3"""
        if not self.client:
            return self._mock_satellite_data(coordinates)
        
        try:
            # In production, this would fetch actual satellite data
            lat, lon = coordinates['lat'], coordinates['lon']
            key = f"satellite-data/{lat:.2f}_{lon:.2f}/ndvi_latest.json"
            
            response = self.client.get_object(Bucket=self.bucket_name, Key=key)
            data = json.loads(response['Body'].read())
            
            return data
            
        except ClientError as e:
            logger.warning(f"Satellite data not found, using mock data: {str(e)}")
            return self._mock_satellite_data(coordinates)
    
    def _mock_satellite_data(self, coordinates: Dict) -> Dict:
        """Mock satellite data when S3 is unavailable"""
        return {
            "ndvi": np.random.uniform(0.2, 0.8),
            "coordinates": coordinates,
            "date": "2024-02-15",
            "source": "Mock Sentinel-2",
            "cloud_cover": np.random.uniform(0, 30)
        }

class DynamoDBService:
    """AWS DynamoDB integration for user scores and metadata"""
    
    def __init__(self, region_name: str = 'ap-south-1', table_name: str = 'gramscore-users'):
        self.region_name = region_name
        self.table_name = table_name
        self.client = None
        self.table = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize DynamoDB client"""
        try:
            dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
            self.table = dynamodb.Table(self.table_name)
            logger.info(f"DynamoDB table initialized: {self.table_name}")
        except Exception as e:
            logger.error(f"Failed to initialize DynamoDB: {str(e)}")
            self.table = None
    
    def store_user_score(self, user_id: str, score_data: Dict) -> bool:
        """Store user score in DynamoDB"""
        if not self.table:
            logger.warning("DynamoDB table not available, score not stored")
            return False
        
        try:
            item = {
                'user_id': user_id,
                'gramscore': score_data['score'],
                'components': score_data['components'],
                'confidence': score_data['confidence'],
                'timestamp': score_data['timestamp'],
                'ttl': int(score_data['timestamp']) + (90 * 24 * 60 * 60)  # 90 days TTL
            }
            
            self.table.put_item(Item=item)
            logger.info(f"Score stored for user: {user_id}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to store score: {str(e)}")
            return False
    
    def get_user_score(self, user_id: str) -> Optional[Dict]:
        """Retrieve user score from DynamoDB"""
        if not self.table:
            return None
        
        try:
            response = self.table.get_item(Key={'user_id': user_id})
            return response.get('Item')
            
        except ClientError as e:
            logger.error(f"Failed to retrieve score: {str(e)}")
            return None

class AWSServicesOrchestrator:
    """Main orchestrator for all AWS services"""
    
    def __init__(self, region_name: str = 'ap-south-1'):
        self.region_name = region_name
        self.bedrock = BedrockService(region_name)
        self.sagemaker = SageMakerService(region_name)
        self.s3 = S3DataService(region_name)
        self.dynamodb = DynamoDBService(region_name)
    
    def calculate_comprehensive_score(self, user_data: Dict) -> Dict:
        """Calculate comprehensive GramScore using all AWS services"""
        
        # Prepare features for ML model
        features = [
            user_data.get('upi_consistency', 0),
            user_data.get('ndvi_avg', 0) * 100,  # Scale NDVI to 0-100
            user_data.get('utility_payment_score', 0),
            user_data.get('psychometric_score', 0)
        ]
        
        # Get ML prediction from SageMaker
        ml_prediction = self.sagemaker.predict_credit_score(features)
        
        # Get AI insights from Bedrock
        ai_insights = self.bedrock.generate_credit_insights(user_data)
        
        # Store satellite data (if available)
        if 'location' in user_data:
            satellite_data = self.s3.retrieve_satellite_data(user_data['location']['coordinates'])
        else:
            satellite_data = None
        
        # Combine results
        result = {
            "gramscore": ml_prediction['predicted_score'],
            "confidence": ml_prediction['confidence'],
            "components": ml_prediction['feature_importance'],
            "ai_insights": ai_insights['insights'],
            "satellite_data": satellite_data,
            "timestamp": int(np.datetime64('now').astype(int) / 1e9),
            "aws_services_used": {
                "sagemaker": ml_prediction['source'],
                "bedrock": ai_insights['source'],
                "s3": "satellite data" if satellite_data else "not used",
                "dynamodb": "score storage"
            }
        }
        
        # Store score in DynamoDB
        if 'user_id' in user_data:
            self.dynamodb.store_user_score(user_data['user_id'], result)
        
        return result
    
    def health_check(self) -> Dict:
        """Check health of all AWS services"""
        return {
            "bedrock": self.bedrock.client is not None,
            "sagemaker": self.sagemaker.client is not None,
            "s3": self.s3.client is not None,
            "dynamodb": self.dynamodb.table is not None,
            "region": self.region_name
        }