import React, { useState, useEffect } from 'react';
import { Mic, Square, RefreshCw, CheckCircle, Volume2 } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import './VoiceAssessment.css';

const questions = {
  en: [
    { id: 1, text: 'If your crop fails, how will you repay your loan?', sub: '' },
    { id: 2, text: 'What will you do with the profits when your business succeeds?', sub: '' },
  ],
  hi: [
    { id: 1, text: 'यदि आपकी फसल खराब हो जाए, तो आप अपना लोन कैसे चुकाएंगे?', sub: 'If your crop fails, how will you repay your loan?' },
    { id: 2, text: 'व्यापार में मुनाफा होने पर आप उन पैसों का क्या करेंगे?', sub: 'What will you do with the profits when your business succeeds?' },
  ],
  mr: [
    { id: 1, text: 'जर तुमची पीक नापीक झाली, तर तुम्ही कर्ज कसे फेडणार?', sub: 'If your crop fails, how will you repay your loan?' },
    { id: 2, text: 'व्यापारात नफा झाल्यावर तुम्ही ते पैसे कुठे वापरणार?', sub: 'What will you do with the profits when your business succeeds?' },
  ],
  te: [
    { id: 1, text: 'మీ పంట వైఫల్యం అయితే, మీరు రుణాన్ని ఎలా చెల్లిస్తారు?', sub: 'If your crop fails, how will you repay your loan?' },
    { id: 2, text: 'వ్యాపారంలో లాభం వస్తే మీరు ఆ డబ్బుని ఎలా వాడతారు?', sub: 'What will you do with the profits when your business succeeds?' },
  ],
  ta: [
    { id: 1, text: 'உங்கள் பயிர் தோல்வியடைந்தால், கடனை எவ்வாறு திருப்பிச் செலுத்துவீர்கள்?', sub: 'If your crop fails, how will you repay your loan?' },
    { id: 2, text: 'வணிகம் வெற்றி பெற்றால் லாப பணத்தை என்ன செய்வீர்கள்?', sub: 'What will you do with the profits when your business succeeds?' },
  ],
  kn: [
    { id: 1, text: 'ನಿಮ್ಮ ಬೆಳೆ ವಿಫಲವಾದರೆ, ಸಾಲವನ್ನು ಹೇಗೆ ಮರುಪಾವತಿ ಮಾಡುತ್ತೀರಿ?', sub: 'If your crop fails, how will you repay your loan?' },
    { id: 2, text: 'ವ್ಯಾಪಾರದಲ್ಲಿ ಲಾಭ ಬಂದಾಗ ಆ ಹಣವನ್ನು ಹೇಗೆ ಬಳಸುತ್ತೀರಿ?', sub: 'What will you do with the profits when your business succeeds?' },
  ],
};

const VoiceAssessment = () => {
  const { lang, t } = useLanguage();
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState(0);

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
    setTimeout(() => {
      setIsProcessing(false);
      if (currentQuestion < currentQs.length - 1) {
        setCurrentQuestion(p => p + 1);
        setRecordingTime(0);
      } else {
        setIsComplete(true);
      }
    }, 2000);
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

          <div className="recording-interface text-center">
            {isProcessing ? (
              <div className="processing-state">
                <RefreshCw size={44} className="animate-spin" />
                <p>{t.assessment.analyzing}</p>
              </div>
            ) : (
              <div className="recording-state">
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
