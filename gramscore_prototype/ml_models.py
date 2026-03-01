"""
Machine Learning Models for GramScore AI
Includes XGBoost, Random Forest, and other ML algorithms for credit scoring
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import joblib
import json
from typing import Dict, List, Tuple, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GramScoreMLModel:
    """Base class for GramScore ML models"""
    
    def __init__(self, model_type: str = 'xgboost'):
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'upi_consistency',
            'transaction_volume_normalized',
            'ndvi_avg',
            'utility_payment_score',
            'psychometric_score',
            'weather_impact',
            'land_size_normalized',
            'crop_diversity_score',
            'seasonal_consistency',
            'digital_literacy_score'
        ]
        self.is_trained = False
    
    def _initialize_model(self):
        """Initialize the ML model based on type"""
        if self.model_type == 'xgboost':
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                objective='reg:squarederror'
            )
        elif self.model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
        elif self.model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            )
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
    
    def generate_synthetic_data(self, n_samples: int = 10000) -> pd.DataFrame:
        """Generate synthetic training data for the model"""
        np.random.seed(42)
        
        data = []
        
        for i in range(n_samples):
            # Generate correlated features that make business sense
            
            # Base farmer profile
            farmer_type = np.random.choice(['reliable', 'moderate', 'high_risk'], p=[0.3, 0.5, 0.2])
            
            if farmer_type == 'reliable':
                upi_consistency = np.random.normal(85, 10)
                transaction_volume = np.random.lognormal(10, 0.5)
                ndvi_avg = np.random.normal(0.7, 0.1)
                utility_score = np.random.normal(85, 10)
                psychometric = np.random.normal(80, 10)
                weather_impact = np.random.normal(0.9, 0.1)
                land_size = np.random.lognormal(1, 0.5)
                
            elif farmer_type == 'moderate':
                upi_consistency = np.random.normal(65, 15)
                transaction_volume = np.random.lognormal(9, 0.7)
                ndvi_avg = np.random.normal(0.5, 0.15)
                utility_score = np.random.normal(70, 15)
                psychometric = np.random.normal(65, 15)
                weather_impact = np.random.normal(0.8, 0.15)
                land_size = np.random.lognormal(0.5, 0.7)
                
            else:  # high_risk
                upi_consistency = np.random.normal(40, 15)
                transaction_volume = np.random.lognormal(8, 0.8)
                ndvi_avg = np.random.normal(0.3, 0.15)
                utility_score = np.random.normal(50, 20)
                psychometric = np.random.normal(45, 20)
                weather_impact = np.random.normal(0.6, 0.2)
                land_size = np.random.lognormal(0, 0.8)
            
            # Clip values to realistic ranges
            upi_consistency = np.clip(upi_consistency, 0, 100)
            ndvi_avg = np.clip(ndvi_avg, 0, 1)
            utility_score = np.clip(utility_score, 0, 100)
            psychometric = np.clip(psychometric, 0, 100)
            weather_impact = np.clip(weather_impact, 0.2, 1.2)
            land_size = np.clip(land_size, 0, 10)
            transaction_volume = np.clip(transaction_volume, 1000, 100000)
            
            # Derived features
            crop_diversity = min(int(land_size) + 1, 5) + np.random.randint(-1, 2)
            crop_diversity = max(1, crop_diversity)
            
            seasonal_consistency = upi_consistency * np.random.uniform(0.8, 1.2)
            seasonal_consistency = np.clip(seasonal_consistency, 0, 100)
            
            digital_literacy = (upi_consistency + psychometric) / 2 + np.random.normal(0, 10)
            digital_literacy = np.clip(digital_literacy, 0, 100)
            
            # Calculate target GramScore
            score_components = {
                'transaction': upi_consistency * 0.30,
                'agriculture': (ndvi_avg * 100) * 0.30,
                'utility': utility_score * 0.20,
                'psychometric': psychometric * 0.20
            }
            
            base_score = sum(score_components.values())
            
            # Apply adjustments
            weather_adjustment = weather_impact
            volume_adjustment = min(1.1, np.log(transaction_volume / 10000) * 0.1 + 1)
            land_adjustment = min(1.1, land_size * 0.05 + 1)
            
            final_score = base_score * weather_adjustment * volume_adjustment * land_adjustment
            final_score = int(300 + (final_score * 6))  # Scale to 300-900
            final_score = np.clip(final_score, 300, 900)
            
            # Add some noise
            final_score += np.random.normal(0, 20)
            final_score = np.clip(final_score, 300, 900)
            
            data.append({
                'upi_consistency': upi_consistency,
                'transaction_volume_normalized': np.log(transaction_volume),
                'ndvi_avg': ndvi_avg,
                'utility_payment_score': utility_score,
                'psychometric_score': psychometric,
                'weather_impact': weather_impact,
                'land_size_normalized': np.log(land_size + 1),
                'crop_diversity_score': crop_diversity,
                'seasonal_consistency': seasonal_consistency,
                'digital_literacy_score': digital_literacy,
                'gramscore': final_score,
                'farmer_type': farmer_type
            })
        
        return pd.DataFrame(data)
    
    def train(self, data: pd.DataFrame = None) -> Dict:
        """Train the ML model"""
        if data is None:
            logger.info("Generating synthetic training data...")
            data = self.generate_synthetic_data()
        
        # Prepare features and target
        X = data[self.feature_names]
        y = data['gramscore']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Initialize and train model
        self._initialize_model()
        
        logger.info(f"Training {self.model_type} model...")
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        train_pred = self.model.predict(X_train_scaled)
        test_pred = self.model.predict(X_test_scaled)
        
        metrics = {
            'train_rmse': np.sqrt(mean_squared_error(y_train, train_pred)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, test_pred)),
            'train_r2': r2_score(y_train, train_pred),
            'test_r2': r2_score(y_test, test_pred),
            'train_mae': mean_absolute_error(y_train, train_pred),
            'test_mae': mean_absolute_error(y_test, test_pred)
        }
        
        # Cross-validation
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train, 
            cv=5, scoring='neg_mean_squared_error'
        )
        metrics['cv_rmse_mean'] = np.sqrt(-cv_scores.mean())
        metrics['cv_rmse_std'] = np.sqrt(cv_scores.std())
        
        self.is_trained = True
        
        logger.info(f"Model training completed. Test R²: {metrics['test_r2']:.3f}")
        return metrics
    
    def predict(self, features: Dict) -> Dict:
        """Predict GramScore for given features"""
        if not self.is_trained:
            logger.warning("Model not trained, using fallback prediction")
            return self._fallback_prediction(features)
        
        # Prepare feature vector
        feature_vector = self._prepare_features(features)
        feature_vector_scaled = self.scaler.transform([feature_vector])
        
        # Make prediction
        predicted_score = self.model.predict(feature_vector_scaled)[0]
        predicted_score = np.clip(predicted_score, 300, 900)
        
        # Calculate feature importance (for tree-based models)
        feature_importance = self._get_feature_importance()
        
        # Calculate prediction confidence
        confidence = self._calculate_confidence(feature_vector_scaled)
        
        return {
            'predicted_score': int(predicted_score),
            'confidence': confidence,
            'feature_importance': feature_importance,
            'model_type': self.model_type,
            'features_used': dict(zip(self.feature_names, feature_vector))
        }
    
    def _prepare_features(self, features: Dict) -> List[float]:
        """Prepare feature vector from input dictionary"""
        feature_vector = []
        
        for feature_name in self.feature_names:
            if feature_name == 'upi_consistency':
                feature_vector.append(features.get('upi_consistency', 50))
            elif feature_name == 'transaction_volume_normalized':
                volume = features.get('transaction_volume', 10000)
                feature_vector.append(np.log(max(volume, 1000)))
            elif feature_name == 'ndvi_avg':
                feature_vector.append(features.get('ndvi_avg', 0.4))
            elif feature_name == 'utility_payment_score':
                feature_vector.append(features.get('utility_payment_score', 60))
            elif feature_name == 'psychometric_score':
                feature_vector.append(features.get('psychometric_score', 60))
            elif feature_name == 'weather_impact':
                feature_vector.append(features.get('weather_impact', 0.8))
            elif feature_name == 'land_size_normalized':
                land_size = features.get('land_size', 1)
                feature_vector.append(np.log(max(land_size, 0.1) + 1))
            elif feature_name == 'crop_diversity_score':
                crops = features.get('crop_types', [])
                feature_vector.append(len(crops) if crops else 1)
            elif feature_name == 'seasonal_consistency':
                # Derived from UPI consistency with some variation
                base = features.get('upi_consistency', 50)
                feature_vector.append(base * np.random.uniform(0.9, 1.1))
            elif feature_name == 'digital_literacy_score':
                # Average of UPI and psychometric scores
                upi = features.get('upi_consistency', 50)
                psych = features.get('psychometric_score', 60)
                feature_vector.append((upi + psych) / 2)
            else:
                feature_vector.append(0)  # Default value
        
        return feature_vector
    
    def _get_feature_importance(self) -> Dict:
        """Get feature importance from trained model"""
        if hasattr(self.model, 'feature_importances_'):
            importance = self.model.feature_importances_
            return dict(zip(self.feature_names, importance))
        else:
            # Default importance for non-tree models
            return {
                'upi_consistency': 0.25,
                'ndvi_avg': 0.25,
                'utility_payment_score': 0.20,
                'psychometric_score': 0.15,
                'transaction_volume_normalized': 0.10,
                'weather_impact': 0.05
            }
    
    def _calculate_confidence(self, feature_vector_scaled: np.ndarray) -> float:
        """Calculate prediction confidence"""
        # For tree-based models, use prediction variance
        if hasattr(self.model, 'estimators_'):
            predictions = []
            for estimator in self.model.estimators_[:10]:  # Sample first 10 trees
                if hasattr(estimator, 'predict'):
                    pred = estimator.predict(feature_vector_scaled)[0]
                    predictions.append(pred)
            
            if predictions:
                variance = np.var(predictions)
                # Convert variance to confidence (inverse relationship)
                confidence = max(0.5, 1 - (variance / 10000))
                return min(0.95, confidence)
        
        # Default confidence
        return 0.85
    
    def _fallback_prediction(self, features: Dict) -> Dict:
        """Fallback prediction when model is not trained"""
        # Simple weighted average
        weights = {
            'upi_consistency': 0.30,
            'ndvi_avg': 0.30,
            'utility_payment_score': 0.20,
            'psychometric_score': 0.20
        }
        
        weighted_score = 0
        for feature, weight in weights.items():
            if feature == 'ndvi_avg':
                value = features.get(feature, 0.4) * 100
            else:
                value = features.get(feature, 50)
            weighted_score += value * weight
        
        final_score = int(300 + (weighted_score * 6))
        final_score = np.clip(final_score, 300, 900)
        
        return {
            'predicted_score': final_score,
            'confidence': 0.70,
            'feature_importance': weights,
            'model_type': 'fallback',
            'features_used': features
        }
    
    def save_model(self, filepath: str):
        """Save trained model to file"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'model_type': self.model_type,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model from file"""
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.model_type = model_data['model_type']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']
        
        logger.info(f"Model loaded from {filepath}")

class EnsembleGramScoreModel:
    """Ensemble model combining multiple ML algorithms"""
    
    def __init__(self):
        self.models = {
            'xgboost': GramScoreMLModel('xgboost'),
            'random_forest': GramScoreMLModel('random_forest'),
            'gradient_boosting': GramScoreMLModel('gradient_boosting')
        }
        self.weights = {'xgboost': 0.5, 'random_forest': 0.3, 'gradient_boosting': 0.2}
        self.is_trained = False
    
    def train(self, data: pd.DataFrame = None) -> Dict:
        """Train all models in the ensemble"""
        all_metrics = {}
        
        for name, model in self.models.items():
            logger.info(f"Training {name} model...")
            metrics = model.train(data)
            all_metrics[name] = metrics
        
        self.is_trained = True
        return all_metrics
    
    def predict(self, features: Dict) -> Dict:
        """Make ensemble prediction"""
        if not self.is_trained:
            # Use the first model as fallback
            return self.models['xgboost'].predict(features)
        
        predictions = {}
        weighted_score = 0
        total_weight = 0
        combined_importance = {}
        
        for name, model in self.models.items():
            pred = model.predict(features)
            predictions[name] = pred
            
            weight = self.weights[name] * pred['confidence']
            weighted_score += pred['predicted_score'] * weight
            total_weight += weight
            
            # Combine feature importance
            for feature, importance in pred['feature_importance'].items():
                if feature not in combined_importance:
                    combined_importance[feature] = 0
                combined_importance[feature] += importance * weight
        
        # Normalize
        if total_weight > 0:
            final_score = weighted_score / total_weight
            combined_importance = {k: v/total_weight for k, v in combined_importance.items()}
        else:
            final_score = 500  # Default score
        
        # Calculate ensemble confidence
        score_variance = np.var([p['predicted_score'] for p in predictions.values()])
        confidence = max(0.7, 1 - (score_variance / 10000))
        
        return {
            'predicted_score': int(np.clip(final_score, 300, 900)),
            'confidence': min(0.95, confidence),
            'feature_importance': combined_importance,
            'model_type': 'ensemble',
            'individual_predictions': predictions,
            'ensemble_weights': self.weights
        }

# Utility functions for model evaluation and deployment
def evaluate_model_performance(model: GramScoreMLModel, test_data: pd.DataFrame) -> Dict:
    """Evaluate model performance on test data"""
    X_test = test_data[model.feature_names]
    y_true = test_data['gramscore']
    
    predictions = []
    for _, row in X_test.iterrows():
        features = row.to_dict()
        pred = model.predict(features)
        predictions.append(pred['predicted_score'])
    
    y_pred = np.array(predictions)
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    # Score distribution analysis
    score_ranges = {
        'excellent (750-900)': ((y_pred >= 750) & (y_pred <= 900)).sum(),
        'good (650-749)': ((y_pred >= 650) & (y_pred < 750)).sum(),
        'fair (550-649)': ((y_pred >= 550) & (y_pred < 650)).sum(),
        'poor (300-549)': ((y_pred >= 300) & (y_pred < 550)).sum()
    }
    
    return {
        'rmse': rmse,
        'mae': mae,
        'r2_score': r2,
        'score_distribution': score_ranges,
        'mean_prediction': np.mean(y_pred),
        'std_prediction': np.std(y_pred)
    }

def create_model_explanation(prediction_result: Dict, language: str = 'en') -> str:
    """Create human-readable explanation of the prediction"""
    score = prediction_result['predicted_score']
    importance = prediction_result['feature_importance']
    
    # Sort features by importance
    sorted_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    
    explanations = {
        'en': {
            'intro': f"Your GramScore of {score} is calculated based on:",
            'features': {
                'upi_consistency': "UPI transaction consistency",
                'ndvi_avg': "Agricultural productivity (satellite data)",
                'utility_payment_score': "Utility bill payment history",
                'psychometric_score': "Financial behavior assessment"
            }
        },
        'hi': {
            'intro': f"आपका GramScore {score} इन आधारों पर बना है:",
            'features': {
                'upi_consistency': "UPI लेनदेन की नियमितता",
                'ndvi_avg': "कृषि उत्पादकता (उपग्रह डेटा)",
                'utility_payment_score': "बिजली बिल भुगतान का इतिहास",
                'psychometric_score': "वित्तीय व्यवहार का आकलन"
            }
        }
    }
    
    lang_data = explanations.get(language, explanations['en'])
    explanation = lang_data['intro'] + "\n\n"
    
    for feature, imp in sorted_features[:4]:  # Top 4 features
        feature_name = lang_data['features'].get(feature, feature)
        impact = int(imp * 100)
        explanation += f"• {feature_name}: {impact}% प्रभाव\n"
    
    return explanation