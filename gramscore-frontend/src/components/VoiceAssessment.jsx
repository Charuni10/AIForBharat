import React, { useState, useEffect, useRef } from 'react';
import { Mic, Square, RefreshCw, CheckCircle, Volume2, MessageSquare, Send } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../services/api';
import './VoiceAssessment.css';

const questions = {
  en: [
    { id: 1, text: 'How do you typically plan your monthly expenses?', sub: '', category: 'financial_discipline', keywords: ['budget', 'plan', 'save', 'track', 'record'] },
    { id: 2, text: 'What would you do if you had an unexpected expense of ₹5000?', sub: '', category: 'risk_awareness', keywords: ['borrow', 'save', 'family', 'loan', 'emergency'] },
    { id: 3, text: 'How do you decide when to invest in new farming equipment?', sub: '', category: 'planning_ability', keywords: ['profit', 'need', 'season', 'money', 'benefit'] },
    { id: 4, text: 'Describe your experience with digital payments like UPI.', sub: '', category: 'digital_literacy', keywords: ['easy', 'use', 'phone', 'payment', 'app'] },
    { id: 5, text: 'How confident are you about repaying a loan on time?', sub: '', category: 'confidence_level', keywords: ['confident', 'sure', 'definitely', 'always', 'never'] },
  ],
  hi: [
    { id: 1, text: 'आप आमतौर पर अपने मासिक खर्चों की योजना कैसे बनाते हैं?', sub: 'How do you typically plan your monthly expenses?', category: 'financial_discipline', keywords: ['बजट', 'योजना', 'बचत', 'ट्रैक', 'रिकॉर्ड'] },
    { id: 2, text: 'यदि आपको ₹5000 का अप्रत्याशित खर्च करना पड़े तो आप क्या करेंगे?', sub: 'What would you do if you had an unexpected expense of ₹5000?', category: 'risk_awareness', keywords: ['उधार', 'बचत', 'परिवार', 'लोन', 'आपातकाल'] },
    { id: 3, text: 'आप नए कृषि उपकरण में निवेश करने का निर्णय कैसे लेते हैं?', sub: 'How do you decide when to invest in new farming equipment?', category: 'planning_ability', keywords: ['लाभ', 'जरूरत', 'मौसम', 'पैसा', 'फायदा'] },
    { id: 4, text: 'UPI जैसे डिजिटल भुगतान के साथ आपका अनुभव कैसा है?', sub: 'Describe your experience with digital payments like UPI.', category: 'digital_literacy', keywords: ['आसान', 'उपयोग', 'फोन', 'भुगतान', 'ऐप'] },
    { id: 5, text: 'समय पर लोन चुकाने के बारे में आप कितने आत्मविश्वास से भरे हैं?', sub: 'How confident are you about repaying a loan on time?', category: 'confidence_level', keywords: ['आत्मविश्वास', 'यकीन', 'जरूर', 'हमेशा', 'कभी नहीं'] },
  ],
  mr: [
    { id: 1, text: 'तुम्ही सामान्यतः तुमच्या मासिक खर्चाची योजना कशी करता?', sub: 'How do you typically plan your monthly expenses?', category: 'financial_discipline', keywords: ['बजेट', 'योजना', 'बचत', 'ट्रॅक', 'रेकॉर्ड'] },
    { id: 2, text: 'जर तुम्हाला ₹5000 चा अनपेक्षित खर्च करावा लागला तर तुम्ही काय कराल?', sub: 'What would you do if you had an unexpected expense of ₹5000?', category: 'risk_awareness', keywords: ['कर्ज', 'बचत', 'कुटुंब', 'लोन', 'आपत्कालीन'] },
    { id: 3, text: 'नवीन शेती उपकरणांमध्ये गुंतवणूक करण्याचा निर्णय तुम्ही कसा घेता?', sub: 'How do you decide when to invest in new farming equipment?', category: 'planning_ability', keywords: ['नफा', 'गरज', 'हंगाम', 'पैसा', 'फायदा'] },
    { id: 4, text: 'UPI सारख्या डिजिटल पेमेंटचा तुमचा अनुभव कसा आहे?', sub: 'Describe your experience with digital payments like UPI.', category: 'digital_literacy', keywords: ['सोपे', 'वापर', 'फोन', 'पेमेंट', 'अॅप'] },
    { id: 5, text: 'वेळेवर लोन परत करण्याबद्दल तुम्ही किती आत्मविश्वासाने भरलेले आहात?', sub: 'How confident are you about repaying a loan on time?', category: 'confidence_level', keywords: ['आत्मविश्वास', 'खात्री', 'नक्की', 'नेहमी', 'कधीच नाही'] },
  ],
  te: [
    { id: 1, text: 'మీరు సాధారణంగా మీ నెలవారీ ఖర్చులను ఎలా ప్లాన్ చేస్తారు?', sub: 'How do you typically plan your monthly expenses?', category: 'financial_discipline', keywords: ['బడ్జెట్', 'ప్లాన్', 'సేవ్', 'ట్రాక్', 'రికార్డ్'] },
    { id: 2, text: 'మీకు ₹5000 అనుకోని ఖర్చు వస్తే మీరు ఏమి చేస్తారు?', sub: 'What would you do if you had an unexpected expense of ₹5000?', category: 'risk_awareness', keywords: ['అప్పు', 'సేవ్', 'కుటుంబం', 'లోన్', 'ఎమర్జెన్సీ'] },
    { id: 3, text: 'కొత్త వ్యవసాయ పరికరాలలో పెట్టుబడి పెట్టాలని మీరు ఎలా నిర్ణయిస్తారు?', sub: 'How do you decide when to invest in new farming equipment?', category: 'planning_ability', keywords: ['లాభం', 'అవసరం', 'సీజన్', 'డబ్బు', 'ప్రయోజనం'] },
    { id: 4, text: 'UPI వంటి డిజిటల్ చెల్లింపులతో మీ అనుభవం ఎలా ఉంది?', sub: 'Describe your experience with digital payments like UPI.', category: 'digital_literacy', keywords: ['సులభం', 'ఉపయోగం', 'ఫోన్', 'చెల్లింపు', 'యాప్'] },
    { id: 5, text: 'సమయానికి లోన్ తిరిగి చెల్లించడంలో మీకు ఎంత నమ్మకం ఉంది?', sub: 'How confident are you about repaying a loan on time?', category: 'confidence_level', keywords: ['నమ్మకం', 'ఖచ్చితంగా', 'తప్పకుండా', 'ఎల్లప్పుడూ', 'ఎప్పుడూ కాదు'] },
  ],
  ta: [
    { id: 1, text: 'நீங்கள் பொதுவாக உங்கள் மாதாந்திர செலவுகளை எவ்வாறு திட்டமிடுகிறீர்கள்?', sub: 'How do you typically plan your monthly expenses?', category: 'financial_discipline', keywords: ['பட்ஜெட்', 'திட்டம்', 'சேமிப்பு', 'கண்காணிப்பு', 'பதிவு'] },
    { id: 2, text: 'உங்களுக்கு ₹5000 எதிர்பாராத செலவு வந்தால் என்ன செய்வீர்கள்?', sub: 'What would you do if you had an unexpected expense of ₹5000?', category: 'risk_awareness', keywords: ['கடன்', 'சேமிப்பு', 'குடும்பம்', 'கடன்', 'அவசரம்'] },
    { id: 3, text: 'புதிய விவசாய உபகரணங்களில் முதலீடு செய்ய நீங்கள் எவ்வாறு முடிவு செய்கிறீர்கள்?', sub: 'How do you decide when to invest in new farming equipment?', category: 'planning_ability', keywords: ['லாபம்', 'தேவை', 'பருவம்', 'பணம்', 'நன்மை'] },
    { id: 4, text: 'UPI போன்ற டிஜிட்டல் கட்டணங்களில் உங்கள் அனுபவம் எப்படி?', sub: 'Describe your experience with digital payments like UPI.', category: 'digital_literacy', keywords: ['எளிதானது', 'பயன்பாடு', 'தொலைபேசி', 'கட்டணம்', 'ஆப்'] },
    { id: 5, text: 'சரியான நேரத்தில் கடனை திருப்பிச் செலுத்துவதில் உங்களுக்கு எவ்வளவு நம்பிக்கை உள்ளது?', sub: 'How confident are you about repaying a loan on time?', category: 'confidence_level', keywords: ['நம்பிக்கை', 'உறுதி', 'நிச்சயமாக', 'எப்போதும்', 'ஒருபோதும்'] },
  ],
  kn: [
    { id: 1, text: 'ನೀವು ಸಾಮಾನ್ಯವಾಗಿ ನಿಮ್ಮ ಮಾಸಿಕ ಖರ್ಚುಗಳನ್ನು ಹೇಗೆ ಯೋಜಿಸುತ್ತೀರಿ?', sub: 'How do you typically plan your monthly expenses?', category: 'financial_discipline', keywords: ['ಬಜೆಟ್', 'ಯೋಜನೆ', 'ಉಳಿತಾಯ', 'ಟ್ರ್ಯಾಕ್', 'ರೆಕಾರ್ಡ್'] },
    { id: 2, text: 'ನಿಮಗೆ ₹5000 ಅನಿರೀಕ್ಷಿತ ಖರ್ಚು ಬಂದರೆ ನೀವು ಏನು ಮಾಡುತ್ತೀರಿ?', sub: 'What would you do if you had an unexpected expense of ₹5000?', category: 'risk_awareness', keywords: ['ಸಾಲ', 'ಉಳಿತಾಯ', 'ಕುಟುಂಬ', 'ಲೋನ್', 'ತುರ್ತು'] },
    { id: 3, text: 'ಹೊಸ ಕೃಷಿ ಉಪಕರಣಗಳಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡಲು ನೀವು ಹೇಗೆ ನಿರ್ಧರಿಸುತ್ತೀರಿ?', sub: 'How do you decide when to invest in new farming equipment?', category: 'planning_ability', keywords: ['ಲಾಭ', 'ಅವಶ್ಯಕತೆ', 'ಋತು', 'ಹಣ', 'ಪ್ರಯೋಜನ'] },
    { id: 4, text: 'UPI ನಂತಹ ಡಿಜಿಟಲ್ ಪಾವತಿಗಳೊಂದಿಗೆ ನಿಮ್ಮ ಅನುಭವ ಹೇಗಿದೆ?', sub: 'Describe your experience with digital payments like UPI.', category: 'digital_literacy', keywords: ['ಸುಲಭ', 'ಬಳಕೆ', 'ಫೋನ್', 'ಪಾವತಿ', 'ಆ್ಯಪ್'] },
    { id: 5, text: 'ಸಮಯಕ್ಕೆ ಸಾಲ ಮರುಪಾವತಿ ಮಾಡುವ ಬಗ್ಗೆ ನಿಮಗೆ ಎಷ್ಟು ವಿಶ್ವಾಸವಿದೆ?', sub: 'How confident are you about repaying a loan on time?', category: 'confidence_level', keywords: ['ವಿಶ್ವಾಸ', 'ಖಚಿತ', 'ಖಂಡಿತವಾಗಿ', 'ಯಾವಾಗಲೂ', 'ಎಂದಿಗೂ ಇಲ್ಲ'] },
  ],
};

const VoiceAssessment = () => {
  const { lang, t } = useLanguage();
  const [inputMode, setInputMode] = useState('chat'); // 'chat' or 'voice'
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [responses, setResponses] = useState({});
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [psychometricScore, setPsychometricScore] = useState(null);
  const textareaRef = useRef(null);

  const currentQs = questions[lang] || questions.en;

  useEffect(() => {
    let interval;
    if (isRecording) {
      interval = setInterval(() => setRecordingTime(p => p + 1), 1000);
    }
    return () => clearInterval(interval);
  }, [isRecording]);

  // Reset question index when language changes
  useEffect(() => {
    setCurrentQuestion(0);
    setIsComplete(false);
  }, [lang]);

  const formatTime = (s) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;

  const handleStart = () => { setIsRecording(true); setRecordingTime(0); };

  const handleStop = () => {
    setIsRecording(false);
    setIsProcessing(true);
    
    // Simulate voice processing
    setTimeout(() => {
      setIsProcessing(false);
      
      // Save voice response
      const questionId = `q${currentQuestion + 1}`;
      const currentQ = currentQs[currentQuestion];
      setResponses(prev => ({
        ...prev,
        [questionId]: {
          question: currentQ.text,
          response: `[Voice recording ${recordingTime}s]`,
          category: currentQ.category,
          type: 'voice',
          expected_keywords: currentQ.keywords
        }
      }));
      
      moveToNextQuestion();
    }, 2000);
  };

  const handleChatSubmit = () => {
    if (!currentAnswer.trim()) return;
    
    setIsProcessing(true);
    
    // Save chat response
    const questionId = `q${currentQuestion + 1}`;
    const currentQ = currentQs[currentQuestion];
    setResponses(prev => ({
      ...prev,
      [questionId]: {
        question: currentQ.text,
        response: currentAnswer,
        category: currentQ.category,
        type: 'text',
        expected_keywords: currentQ.keywords
      }
    }));
    
    setCurrentAnswer('');
    
    setTimeout(() => {
      setIsProcessing(false);
      moveToNextQuestion();
    }, 1000);
  };

  const moveToNextQuestion = () => {
    if (currentQuestion < currentQs.length - 1) {
      setCurrentQuestion(p => p + 1);
      setRecordingTime(0);
    } else {
      submitAssessment();
    }
  };

  const submitAssessment = async () => {
    try {
      const result = await api.submitVoiceAssessment({
        responses: responses,
        language: lang
      });
      
      if (result.success) {
        setPsychometricScore(result.psychometric_score);
        setIsComplete(true);
      }
    } catch (error) {
      console.error('Error submitting assessment:', error);
      // Still mark as complete for demo
      setPsychometricScore(75);
      setIsComplete(true);
    }
  };

  const progressPct = (currentQuestion / currentQs.length) * 100;

  return (
    <div className="assessment-container container animate-fade-in">
      <header className="assessment-header text-center">
        <h1>{t.assessment.title}</h1>
        <p className="text-muted">{t.assessment.subtitle}</p>
      </header>

      {isComplete ? (
        <div className="glass-panel complete-card animate-fade-in text-center">
          <div className="success-icon">
            <CheckCircle size={64} />
          </div>
          <h2>{t.assessment.completeTitle}</h2>
          <p className="text-muted">{t.assessment.completeDesc}</p>
          <button className="btn-primary" onClick={() => window.location.href = '/'}>
            {t.assessment.backHome}
          </button>
        </div>
      ) : (
        <div className="glass-panel assessment-card">
          <div className="progress-indicator">
            <span className="progress-label">
              {t.assessment.question} {currentQuestion + 1} {t.assessment.of} {currentQs.length}
            </span>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progressPct}%` }} />
            </div>
          </div>

          <div className="question-display text-center">
            <button className="btn-icon" aria-label={t.assessment.listenBtn}>
              <Volume2 size={22} />
            </button>
            <h3 className="question-text">{currentQs[currentQuestion].text}</h3>
            {currentQs[currentQuestion].sub && (
              <p className="question-sub text-muted">{currentQs[currentQuestion].sub}</p>
            )}
          </div>

          {/* Input Mode Toggle */}
          <div className="input-mode-toggle">
            <button
              className={`mode-btn ${inputMode === 'chat' ? 'active' : ''}`}
              onClick={() => setInputMode('chat')}
              disabled={isProcessing || isRecording}
            >
              <MessageSquare size={20} />
              <span>Chat</span>
            </button>
            <button
              className={`mode-btn ${inputMode === 'voice' ? 'active' : ''}`}
              onClick={() => setInputMode('voice')}
              disabled={isProcessing || isRecording}
            >
              <Mic size={20} />
              <span>Voice</span>
            </button>
          </div>

          {/* Input Interface */}
          <div className="input-interface">
            {isProcessing ? (
              <div className="processing-state">
                <RefreshCw size={44} className="animate-spin" />
                <p>{t.assessment.analyzing}</p>
              </div>
            ) : inputMode === 'chat' ? (
              <div className="chat-interface">
                <div className="chat-input-container">
                  <textarea
                    ref={textareaRef}
                    className="chat-textarea"
                    placeholder={t.assessment.typePlaceholder || "Type your answer here..."}
                    value={currentAnswer}
                    onChange={(e) => setCurrentAnswer(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleChatSubmit();
                      }
                    }}
                    rows={4}
                    disabled={isProcessing}
                  />
                  <button
                    className="btn-send-chat"
                    onClick={handleChatSubmit}
                    disabled={!currentAnswer.trim() || isProcessing}
                    aria-label="Send answer"
                  >
                    <Send size={20} />
                  </button>
                </div>
                <p className="instruction text-muted">
                  {t.assessment.pressEnter || "Press Enter to submit or Shift+Enter for new line"}
                </p>
              </div>
            ) : (
              <div className="voice-interface">
                <div className={`timer-display ${isRecording ? 'recording-active' : ''}`}>
                  {formatTime(recordingTime)}
                </div>
                <div className="controls">
                  {isRecording ? (
                    <button className="btn-stop-record pulse-ring" onClick={handleStop}>
                      <Square size={22} fill="currentColor" />
                    </button>
                  ) : (
                    <button className="btn-start-record" onClick={handleStart}>
                      <Mic size={30} />
                    </button>
                  )}
                </div>
                <p className="instruction text-muted">
                  {isRecording ? t.assessment.tapStop : t.assessment.tapStart}
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default VoiceAssessment;
