"""
Voice-based Psychometric Assessment for GramScore AI
Handles speech-to-text, sentiment analysis, and behavioral assessment
"""

import streamlit as st
import numpy as np
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceAssessmentService:
    """Voice-based psychometric assessment service"""
    
    def __init__(self):
        self.questions = self._load_assessment_questions()
        self.scoring_weights = {
            'financial_discipline': 0.30,
            'risk_awareness': 0.25,
            'planning_ability': 0.20,
            'communication_clarity': 0.15,
            'confidence_level': 0.10
        }
    
    def _load_assessment_questions(self) -> Dict:
        """Load psychometric assessment questions in multiple languages"""
        return {
            'english': [
                {
                    'id': 'q1',
                    'question': 'How do you typically plan your monthly expenses?',
                    'type': 'open_ended',
                    'category': 'financial_discipline',
                    'expected_keywords': ['budget', 'plan', 'save', 'track', 'record']
                },
                {
                    'id': 'q2',
                    'question': 'What would you do if you had an unexpected expense of ₹5000?',
                    'type': 'scenario',
                    'category': 'risk_awareness',
                    'expected_keywords': ['borrow', 'save', 'family', 'loan', 'emergency']
                },
                {
                    'id': 'q3',
                    'question': 'How do you decide when to invest in new farming equipment?',
                    'type': 'decision_making',
                    'category': 'planning_ability',
                    'expected_keywords': ['profit', 'need', 'season', 'money', 'benefit']
                },
                {
                    'id': 'q4',
                    'question': 'Describe your experience with digital payments like UPI.',
                    'type': 'experience',
                    'category': 'digital_literacy',
                    'expected_keywords': ['easy', 'use', 'phone', 'payment', 'app']
                },
                {
                    'id': 'q5',
                    'question': 'How confident are you about repaying a loan on time?',
                    'type': 'confidence',
                    'category': 'confidence_level',
                    'expected_keywords': ['confident', 'sure', 'definitely', 'always', 'never']
                }
            ],
            'hindi': [
                {
                    'id': 'q1',
                    'question': 'आप आमतौर पर अपने मासिक खर्चों की योजना कैसे बनाते हैं?',
                    'type': 'open_ended',
                    'category': 'financial_discipline',
                    'expected_keywords': ['बजट', 'योजना', 'बचत', 'ट्रैक', 'रिकॉर्ड']
                },
                {
                    'id': 'q2',
                    'question': 'यदि आपको ₹5000 का अप्रत्याशित खर्च करना पड़े तो आप क्या करेंगे?',
                    'type': 'scenario',
                    'category': 'risk_awareness',
                    'expected_keywords': ['उधार', 'बचत', 'परिवार', 'लोन', 'आपातकाल']
                },
                {
                    'id': 'q3',
                    'question': 'आप नए कृषि उपकरण में निवेश करने का निर्णय कैसे लेते हैं?',
                    'type': 'decision_making',
                    'category': 'planning_ability',
                    'expected_keywords': ['लाभ', 'जरूरत', 'मौसम', 'पैसा', 'फायदा']
                },
                {
                    'id': 'q4',
                    'question': 'UPI जैसे डिजिटल भुगतान के साथ आपका अनुभव कैसा है?',
                    'type': 'experience',
                    'category': 'digital_literacy',
                    'expected_keywords': ['आसान', 'उपयोग', 'फोन', 'भुगतान', 'ऐप']
                },
                {
                    'id': 'q5',
                    'question': 'समय पर लोन चुकाने के बारे में आप कितने आत्मविश्वास से भरे हैं?',
                    'type': 'confidence',
                    'category': 'confidence_level',
                    'expected_keywords': ['आत्मविश्वास', 'यकीन', 'जरूर', 'हमेशा', 'कभी नहीं']
                }
            ],
            'marathi': [
                {
                    'id': 'q1',
                    'question': 'तुम्ही सामान्यतः तुमच्या मासिक खर्चाची योजना कशी करता?',
                    'type': 'open_ended',
                    'category': 'financial_discipline',
                    'expected_keywords': ['बजेट', 'योजना', 'बचत', 'ट्रॅक', 'रेकॉर्ड']
                },
                {
                    'id': 'q2',
                    'question': 'जर तुम्हाला ₹5000 चा अनपेक्षित खर्च करावा लागला तर तुम्ही काय कराल?',
                    'type': 'scenario',
                    'category': 'risk_awareness',
                    'expected_keywords': ['कर्ज', 'बचत', 'कुटुंब', 'लोन', 'आपत्कालीन']
                },
                {
                    'id': 'q3',
                    'question': 'नवीन शेती उपकरणांमध्ये गुंतवणूक करण्याचा निर्णय तुम्ही कसा घेता?',
                    'type': 'decision_making',
                    'category': 'planning_ability',
                    'expected_keywords': ['नफा', 'गरज', 'हंगाम', 'पैसा', 'फायदा']
                },
                {
                    'id': 'q4',
                    'question': 'UPI सारख्या डिजिटल पेमेंटचा तुमचा अनुभव कसा आहे?',
                    'type': 'experience',
                    'category': 'digital_literacy',
                    'expected_keywords': ['सोपे', 'वापर', 'फोन', 'पेमेंट', 'अॅप']
                },
                {
                    'id': 'q5',
                    'question': 'वेळेवर लोन परत करण्याबद्दल तुम्ही किती आत्मविश्वासाने भरलेले आहात?',
                    'type': 'confidence',
                    'category': 'confidence_level',
                    'expected_keywords': ['आत्मविश्वास', 'खात्री', 'नक्की', 'नेहमी', 'कधीच नाही']
                }
            ]
        }
    
    def create_voice_assessment_ui(self, language: str = 'english') -> Dict:
        """Create Streamlit UI for voice assessment"""
        st.subheader("🎤 Voice-based Psychometric Assessment")
        
        # Language selection
        lang_map = {'English': 'english', 'हिंदी (Hindi)': 'hindi', 'मराठी (Marathi)': 'marathi'}
        selected_lang = lang_map.get(language, 'english')
        
        questions = self.questions[selected_lang]
        responses = {}
        
        st.info("Please answer the following questions. In a real implementation, these would be voice-recorded and processed using speech-to-text.")
        
        for i, question in enumerate(questions):
            st.markdown(f"**Question {i+1}:** {question['question']}")
            
            # Text input for demo (would be voice input in production)
            response = st.text_area(
                f"Your answer (Question {i+1})",
                key=f"voice_q_{question['id']}",
                height=100,
                placeholder="Type your answer here (in production, this would be voice input)..."
            )
            
            if response:
                responses[question['id']] = {
                    'question': question['question'],
                    'response': response,
                    'category': question['category'],
                    'type': question['type'],
                    'expected_keywords': question['expected_keywords']
                }
        
        return responses
    
    def analyze_voice_responses(self, responses: Dict, language: str = 'english') -> Dict:
        """Analyze voice responses and calculate psychometric scores"""
        if not responses:
            return self._default_psychometric_score()
        
        category_scores = {}
        
        for response_id, response_data in responses.items():
            category = response_data['category']
            response_text = response_data['response'].lower()
            expected_keywords = response_data['expected_keywords']
            
            # Keyword matching score
            keyword_matches = sum(1 for keyword in expected_keywords if keyword.lower() in response_text)
            keyword_score = min(100, (keyword_matches / len(expected_keywords)) * 100)
            
            # Response length score (longer responses generally indicate better articulation)
            length_score = min(100, len(response_text.split()) * 5)  # 5 points per word, max 100
            
            # Sentiment analysis (mock implementation)
            sentiment_score = self._analyze_sentiment(response_text)
            
            # Combine scores
            combined_score = (keyword_score * 0.4 + length_score * 0.3 + sentiment_score * 0.3)
            
            if category not in category_scores:
                category_scores[category] = []
            category_scores[category].append(combined_score)
        
        # Calculate final category scores
        final_category_scores = {}
        for category, scores in category_scores.items():
            final_category_scores[category] = np.mean(scores)
        
        # Calculate overall psychometric score
        overall_score = 0
        for category, weight in self.scoring_weights.items():
            category_score = final_category_scores.get(category, 50)  # Default 50 if missing
            overall_score += category_score * weight
        
        return {
            'overall_score': round(overall_score, 1),
            'category_scores': final_category_scores,
            'response_analysis': self._generate_response_analysis(responses, final_category_scores),
            'recommendations': self._generate_recommendations(final_category_scores),
            'assessment_timestamp': datetime.now().isoformat()
        }
    
    def _analyze_sentiment(self, text: str) -> float:
        """Mock sentiment analysis (in production, use AWS Comprehend or similar)"""
        # Simple keyword-based sentiment analysis
        positive_words = ['good', 'confident', 'sure', 'easy', 'always', 'definitely', 'yes', 'plan', 'save']
        negative_words = ['difficult', 'never', 'no', 'hard', 'problem', 'worry', 'scared', 'uncertain']
        
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count + negative_count == 0:
            return 60  # Neutral
        
        sentiment_ratio = positive_count / (positive_count + negative_count)
        return sentiment_ratio * 100
    
    def _generate_response_analysis(self, responses: Dict, category_scores: Dict) -> Dict:
        """Generate detailed analysis of responses"""
        analysis = {
            'total_responses': len(responses),
            'avg_response_length': np.mean([len(r['response'].split()) for r in responses.values()]),
            'strongest_category': max(category_scores.items(), key=lambda x: x[1])[0] if category_scores else None,
            'weakest_category': min(category_scores.items(), key=lambda x: x[1])[0] if category_scores else None,
            'response_quality': 'high' if np.mean(list(category_scores.values())) > 70 else 'medium' if np.mean(list(category_scores.values())) > 50 else 'low'
        }
        
        return analysis
    
    def _generate_recommendations(self, category_scores: Dict) -> List[str]:
        """Generate recommendations based on category scores"""
        recommendations = []
        
        for category, score in category_scores.items():
            if score < 60:
                if category == 'financial_discipline':
                    recommendations.append("Consider creating a monthly budget and tracking expenses")
                elif category == 'risk_awareness':
                    recommendations.append("Build an emergency fund for unexpected expenses")
                elif category == 'planning_ability':
                    recommendations.append("Practice making structured decisions with clear criteria")
                elif category == 'digital_literacy':
                    recommendations.append("Increase familiarity with digital payment systems")
                elif category == 'confidence_level':
                    recommendations.append("Build confidence through small, successful financial commitments")
        
        if not recommendations:
            recommendations.append("Excellent responses! Continue maintaining good financial habits")
        
        return recommendations
    
    def _default_psychometric_score(self) -> Dict:
        """Return default psychometric score when no responses available"""
        return {
            'overall_score': 60.0,
            'category_scores': {
                'financial_discipline': 60,
                'risk_awareness': 60,
                'planning_ability': 60,
                'communication_clarity': 60,
                'confidence_level': 60
            },
            'response_analysis': {
                'total_responses': 0,
                'avg_response_length': 0,
                'response_quality': 'not_assessed'
            },
            'recommendations': ['Complete voice assessment for personalized recommendations'],
            'assessment_timestamp': datetime.now().isoformat()
        }

class SpeechToTextService:
    """Mock Speech-to-Text service (in production, integrate with AWS Transcribe or Azure Speech)"""
    
    def __init__(self, service_provider: str = 'aws_transcribe'):
        self.service_provider = service_provider
        self.supported_languages = ['en-IN', 'hi-IN', 'mr-IN']
    
    def transcribe_audio(self, audio_file_path: str, language: str = 'en-IN') -> Dict:
        """Transcribe audio file to text"""
        # Mock transcription - in production, integrate with actual service
        mock_transcriptions = {
            'en-IN': "I plan my monthly expenses by keeping track of all my income and necessary expenses. I try to save at least 20% of my income for emergencies.",
            'hi-IN': "मैं अपने मासिक खर्चों की योजना अपनी सभी आय और आवश्यक खर्चों का हिसाब रखकर बनाता हूं। मैं आपातकाल के लिए अपनी आय का कम से कम 20% बचाने की कोशिश करता हूं।",
            'mr-IN': "मी माझ्या मासिक खर्चाची योजना माझ्या सर्व उत्पन्न आणि आवश्यक खर्चांचा हिशेब ठेवून करतो. मी आपत्कालीन परिस्थितीसाठी माझ्या उत्पन्नाच्या किमान 20% बचत करण्याचा प्रयत्न करतो."
        }
        
        return {
            'transcription': mock_transcriptions.get(language, mock_transcriptions['en-IN']),
            'confidence': 0.92,
            'language_detected': language,
            'duration_seconds': 45.2,
            'service_provider': self.service_provider
        }
    
    def real_time_transcribe(self, audio_stream) -> str:
        """Real-time transcription for live voice input"""
        # Mock real-time transcription
        return "This is a mock real-time transcription..."

def create_voice_assessment_demo():
    """Create a complete voice assessment demo in Streamlit"""
    st.header("🎤 Voice-based Psychometric Assessment Demo")
    
    # Initialize services
    voice_service = VoiceAssessmentService()
    speech_service = SpeechToTextService()
    
    # Language selection
    language = st.selectbox(
        "Select Language / भाषा चुनें / भाषा निवडा",
        ["English", "हिंदी (Hindi)", "मराठी (Marathi)"]
    )
    
    # Assessment mode
    assessment_mode = st.radio(
        "Assessment Mode",
        ["Text Input (Demo)", "Voice Recording (Mock)"]
    )
    
    if assessment_mode == "Text Input (Demo)":
        # Text-based assessment for demo
        responses = voice_service.create_voice_assessment_ui(language)
        
        if st.button("Analyze Responses", type="primary"):
            if responses:
                with st.spinner("Analyzing responses..."):
                    analysis = voice_service.analyze_voice_responses(responses, language)
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📊 Assessment Results")
                        st.metric("Overall Psychometric Score", f"{analysis['overall_score']}/100")
                        
                        # Category breakdown
                        st.subheader("Category Scores")
                        for category, score in analysis['category_scores'].items():
                            st.metric(category.replace('_', ' ').title(), f"{score:.1f}/100")
                    
                    with col2:
                        st.subheader("📈 Analysis Summary")
                        st.json(analysis['response_analysis'])
                        
                        st.subheader("💡 Recommendations")
                        for rec in analysis['recommendations']:
                            st.info(rec)
            else:
                st.warning("Please answer at least one question to proceed with analysis.")
    
    else:
        # Voice recording mode (mock)
        st.info("🎙️ Voice recording mode is simulated in this demo. In production, this would capture and process real audio.")
        
        if st.button("Start Voice Assessment (Mock)"):
            with st.spinner("Processing voice input..."):
                # Mock voice processing
                mock_audio_path = "mock_audio.wav"
                transcription = speech_service.transcribe_audio(mock_audio_path, 'en-IN')
                
                st.success("Voice transcription completed!")
                st.text_area("Transcribed Text", transcription['transcription'], height=100)
                
                # Mock analysis
                mock_responses = {
                    'q1': {
                        'question': 'How do you plan your monthly expenses?',
                        'response': transcription['transcription'],
                        'category': 'financial_discipline',
                        'type': 'open_ended',
                        'expected_keywords': ['budget', 'plan', 'save', 'track', 'record']
                    }
                }
                
                analysis = voice_service.analyze_voice_responses(mock_responses)
                
                st.subheader("🎯 Voice Assessment Results")
                st.metric("Psychometric Score", f"{analysis['overall_score']}/100")
                
                for rec in analysis['recommendations']:
                    st.info(rec)

if __name__ == "__main__":
    create_voice_assessment_demo()