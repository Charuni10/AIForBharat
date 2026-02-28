import React, { useState, useEffect } from 'react';
import { Activity, MapPin, Zap, Brain, TrendingUp, Clock } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import './Dashboard.css';

const Dashboard = () => {
    const { t } = useLanguage();
    const [animated, setAnimated] = useState(false);
    const targetScore = 720;

    useEffect(() => {
        const timer = setTimeout(() => setAnimated(true), 300);
        return () => clearTimeout(timer);
    }, []);

    const circumference = 2 * Math.PI * 52;
    const scorePercent = ((targetScore - 300) / 600) * 100;
    const dashOffset = animated ? circumference * (1 - scorePercent / 100) : circumference;

    const scoreBand = targetScore >= 750
        ? t.dashboard.excellent_label
        : targetScore >= 650
            ? t.dashboard.good
            : t.dashboard.fair;

    const scoreBandClass = targetScore >= 750 ? 'badge-excellent' : targetScore >= 650 ? 'badge-success' : 'badge-warning';

    const components = [
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
                <div className="header-meta">
                    <Clock size={14} />
                    <span className="text-muted text-sm">
                        {t.dashboard.updated}: {new Date().toLocaleDateString('en-IN')}
                    </span>
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
        </div>
    );
};

export default Dashboard;
