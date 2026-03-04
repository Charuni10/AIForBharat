import React, { useState, useEffect } from 'react';
import { Activity, MapPin, Zap, Brain, TrendingUp, Clock, RefreshCw } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../services/api';
import './Dashboard.css';

const Dashboard = ({ user }) => {
    const { t } = useLanguage();
    const [animated, setAnimated] = useState(false);
    const [loading, setLoading] = useState(false);
    const [apiStatus, setApiStatus] = useState('checking');
    const [scoreData, setScoreData] = useState(null);
    const [targetScore, setTargetScore] = useState(720);
    const [userData, setUserData] = useState({
        upi_consistency: 85,
        transaction_volume: 45000,
        ndvi_avg: 0.7,
        utility_payment_score: 90,
        psychometric_score: 60,
        weather_impact: 0.9,
        land_size: 2.5,
        crop_types: ['Rice', 'Wheat']
    });

    useEffect(() => {
        const timer = setTimeout(() => setAnimated(true), 300);
        checkApiHealth();
        return () => clearTimeout(timer);
    }, []);

    const checkApiHealth = async () => {
        try {
            const health = await api.healthCheck();
            setApiStatus(health.status === 'healthy' ? 'connected' : 'error');
        } catch (error) {
            console.error('API health check failed:', error);
            setApiStatus('disconnected');
        }
    };

    const calculateScore = async () => {
        setLoading(true);
        try {
            const result = await api.calculateScore(userData);
            
            if (result.success) {
                setScoreData(result);
                setTargetScore(result.gramscore);
            } else {
                alert('Failed to calculate score. Please try again.');
            }
        } catch (error) {
            console.error('Error calculating score:', error);
            alert(`Error: ${error.message}\n\nMake sure the Flask API is running on port 5000`);
        } finally {
            setLoading(false);
        }
    };

    const circumference = 2 * Math.PI * 52;
    const scorePercent = ((targetScore - 300) / 600) * 100;
    const dashOffset = animated ? circumference * (1 - scorePercent / 100) : circumference;

    const scoreBand = targetScore >= 750
        ? t.dashboard.excellent_label
        : targetScore >= 650
            ? t.dashboard.good
            : t.dashboard.fair;

    const scoreBandClass = targetScore >= 750 ? 'badge-excellent' : targetScore >= 650 ? 'badge-success' : 'badge-warning';

    const components = scoreData?.components ? [
        { label: t.dashboard.txnFreq, pct: (scoreData.components.transaction_frequency || 0.85) * 100, weight: '30%', color: '#A08C6E', Icon: Activity },
        { label: t.dashboard.agriProd, pct: (scoreData.components.agricultural_productivity || 0.70) * 100, weight: '30%', color: '#7C9B7A', Icon: MapPin },
        { label: t.dashboard.utilityHygiene, pct: (scoreData.components.utility_payments || 0.90) * 100, weight: '20%', color: '#C4934A', Icon: Zap },
        { label: t.dashboard.repayIntent, pct: (scoreData.components.psychometric_score || 0.60) * 100, weight: '20%', color: '#9B7A7A', Icon: Brain },
    ] : [
        { label: t.dashboard.txnFreq, pct: 85, weight: '30%', color: '#A08C6E', Icon: Activity },
        { label: t.dashboard.agriProd, pct: 70, weight: '30%', color: '#7C9B7A', Icon: MapPin },
        { label: t.dashboard.utilityHygiene, pct: 90, weight: '20%', color: '#C4934A', Icon: Zap },
        { label: t.dashboard.repayIntent, pct: 60, weight: '20%', color: '#9B7A7A', Icon: Brain },
    ];

    const recs = [
        { pts: '+15', title: t.dashboard.rec1_title, desc: t.dashboard.rec1_desc },
        { pts: '+10', title: t.dashboard.rec2_title, desc: t.dashboard.rec2_desc },
        { pts: '+8', title: t.dashboard.rec3_title, desc: t.dashboard.rec3_desc },
    ];

    return (
        <div className="dashboard-container container animate-fade-in">
            <header className="dashboard-header">
                <div>
                    <h1>{t.dashboard.greeting}</h1>
                    <p className="text-muted">{t.dashboard.subtitle}</p>
                </div>
                <div className="header-meta" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <button 
                        onClick={calculateScore}
                        disabled={loading || apiStatus !== 'connected'}
                        style={{
                            padding: '0.5rem 1rem',
                            borderRadius: '0.5rem',
                            background: loading ? '#9ca3af' : '#667eea',
                            color: 'white',
                            border: 'none',
                            cursor: loading || apiStatus !== 'connected' ? 'not-allowed' : 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            fontSize: '0.875rem',
                            fontWeight: '500'
                        }}
                    >
                        <RefreshCw size={14} className={loading ? 'spin' : ''} />
                        {loading ? 'Calculating...' : 'Calculate Score'}
                    </button>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Clock size={14} />
                        <span className="text-muted text-sm">
                            {t.dashboard.updated}: {new Date().toLocaleDateString('en-IN')}
                        </span>
                    </div>
                </div>
            </header>

            <div className="dashboard-grid">
                {/* Score Card */}
                <div className="glass-panel score-card">
                    <div className="score-header">
                        <h3>{t.dashboard.yourScore}</h3>
                        <span className={`badge ${scoreBandClass}`}>{scoreBand}</span>
                    </div>

                    <div className="score-gauge">
                        <svg viewBox="0 0 120 120" className="gauge-svg">
                            <defs>
                                <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" stopColor="#A08C6E" />
                                    <stop offset="100%" stopColor="#C4934A" />
                                </linearGradient>
                            </defs>
                            <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(200,175,130,0.1)" strokeWidth="10" />
                            <circle
                                cx="60" cy="60" r="52" fill="none"
                                stroke="url(#scoreGradient)"
                                strokeWidth="10"
                                strokeLinecap="round"
                                strokeDasharray={circumference}
                                strokeDashoffset={dashOffset}
                                style={{ transition: 'stroke-dashoffset 1.5s cubic-bezier(0.4,0,0.2,1)', transform: 'rotate(-90deg)', transformOrigin: '50% 50%' }}
                            />
                        </svg>
                        <div className="gauge-center">
                            <span className="score-number">{animated ? targetScore : 300}</span>
                            <span className="score-out text-muted">/ 900</span>
                        </div>
                    </div>

                    <div className="score-range-labels">
                        <span className="text-muted text-sm">{t.dashboard.poor}</span>
                        <span className="text-muted text-sm">{t.dashboard.excellent}</span>
                    </div>
                </div>

                {/* Breakdown */}
                <div className="glass-panel components-card">
                    <h3>{t.dashboard.breakdown}</h3>
                    <div className="components-list">
                        {components.map(({ label, pct, weight, color, Icon }) => (
                            <div className="component-item" key={label}>
                                <div className="comp-icon" style={{ background: `${color}22`, color }}>
                                    <Icon size={20} />
                                </div>
                                <div className="comp-info">
                                    <div className="comp-label-row">
                                        <span className="comp-label">{label}</span>
                                        <span className="comp-weight text-muted">{weight}</span>
                                    </div>
                                    <div className="progress-bar">
                                        <div
                                            className="progress-fill"
                                            style={{ width: animated ? `${pct}%` : '0%', background: color, transition: 'width 1.2s ease' }}
                                        />
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Recommendations */}
            <div className="glass-panel recommendations-panel">
                <div className="rec-header">
                    <TrendingUp size={20} className="icon-accent" />
                    <h3>{t.dashboard.improve}</h3>
                </div>
                <ul className="recommendations-list">
                    {recs.map(({ pts, title, desc }) => (
                        <li key={title}>
                            <div className="rec-badge">{pts} pts</div>
                            <div className="rec-content">
                                <strong>{title}</strong>
                                <p>{desc}</p>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>

            {/* AI Insights from Backend */}
            {scoreData?.ai_insights && (
                <div className="glass-panel" style={{ marginTop: '1.5rem' }}>
                    <div className="rec-header">
                        <Brain size={20} className="icon-accent" />
                        <h3>🤖 AI Insights (AWS Bedrock)</h3>
                    </div>
                    <div style={{ padding: '1rem', background: 'rgba(102, 126, 234, 0.05)', borderRadius: '0.5rem', marginTop: '1rem' }}>
                        <p style={{ margin: 0, lineHeight: '1.6' }}>{scoreData.ai_insights}</p>
                        <div style={{ marginTop: '1rem', fontSize: '0.75rem', color: '#9ca3af' }}>
                            Model: {scoreData.model_type} | Confidence: {(scoreData.confidence * 100).toFixed(1)}% | 
                            Risk: {scoreData.risk_level}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
