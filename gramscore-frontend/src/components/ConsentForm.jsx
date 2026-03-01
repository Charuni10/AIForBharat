import React, { useState } from 'react';
import { Shield, Smartphone, Satellite, Zap, CheckCircle } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../services/api';
import './ConsentForm.css';

const ConsentForm = () => {
  const { t } = useLanguage();
  const [consents, setConsents] = useState({ upi: false, satellite: false, utility: false });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [consentToken, setConsentToken] = useState(null);

  const toggle = (type) => setConsents(prev => ({ ...prev, [type]: !prev[type] }));

  const handleApproveAll = () => setConsents({ upi: true, satellite: true, utility: true });

  const handleSubmit = async () => {
    setIsSubmitting(true);
    
    try {
      // Prepare consent data
      const dataTypes = [];
      if (consents.upi) dataTypes.push('transactions');
      if (consents.satellite) dataTypes.push('satellite');
      if (consents.utility) dataTypes.push('utilities');
      
      // Submit to backend
      const result = await api.submitConsent({ data_types: dataTypes });
      
      if (result.success) {
        setConsentToken(result.consent_token);
        setIsSuccess(true);
        setTimeout(() => setIsSuccess(false), 3000);
      } else {
        alert('Failed to submit consent. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting consent:', error);
      alert(`Error: ${error.message}\n\nMake sure you're logged in and the API is running.`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const allApproved = Object.values(consents).every(Boolean);
  const noneApproved = Object.values(consents).every(v => !v);

  const sources = [
    {
      key: 'upi',
      Icon: Smartphone,
      colorClass: 'bg-primary-light',
      title: t.consent.upiTitle,
      sub: t.consent.upiSub,
      desc: t.consent.upiDesc,
    },
    {
      key: 'satellite',
      Icon: Satellite,
      colorClass: 'bg-success-light',
      title: t.consent.satTitle,
      sub: t.consent.satSub,
      desc: t.consent.satDesc,
    },
    {
      key: 'utility',
      Icon: Zap,
      colorClass: 'bg-warning-light',
      title: t.consent.utilTitle,
      sub: t.consent.utilSub,
      desc: t.consent.utilDesc,
    },
  ];

  return (
    <div className="consent-container container animate-fade-in">
      <header className="consent-header text-center">
        <div className="shield-icon">
          <Shield size={44} />
        </div>
        <h1>{t.consent.title}</h1>
        <p className="text-muted">{t.consent.subtitle}</p>
      </header>

      <div className="consent-cards-grid">
        {sources.map(({ key, Icon, colorClass, title, sub, desc }) => (
          <div
            key={key}
            className={`glass-panel consent-card ${consents[key] ? 'approved' : ''}`}
          >
            <div className={`consent-icon ${colorClass}`}>
              <Icon size={22} />
            </div>
            <div className="consent-details">
              <h2>{title}</h2>
              <p className="text-sm text-muted">{sub}</p>
              <p className="consent-desc">{desc}</p>
            </div>
            <button
              className={`btn-toggle ${consents[key] ? 'active' : ''}`}
              onClick={() => toggle(key)}
            >
              {consents[key] ? <CheckCircle size={18} /> : t.consent.approve}
            </button>
          </div>
        ))}
      </div>

      <div className="consent-actions glass-panel text-center">
        <h3>{t.consent.ready}</h3>
        {consentToken && (
          <div style={{ 
            padding: '0.75rem', 
            background: 'rgba(16, 185, 129, 0.1)', 
            borderRadius: '0.5rem', 
            marginBottom: '1rem',
            fontSize: '0.875rem'
          }}>
            ✅ Consent recorded! Token: {consentToken.substring(0, 20)}...
          </div>
        )}
        <div className="button-group">
          {!allApproved && (
            <button className="btn-secondary" onClick={handleApproveAll}>
              {t.consent.approveAll}
            </button>
          )}
          <button
            className="btn-primary"
            onClick={handleSubmit}
            disabled={noneApproved || isSubmitting}
          >
            {isSubmitting ? t.consent.processing : isSuccess ? t.consent.saved : t.consent.confirm}
          </button>
        </div>
        <p className="text-xs text-muted">{t.consent.legal}</p>
      </div>
    </div>
  );
};

export default ConsentForm;
