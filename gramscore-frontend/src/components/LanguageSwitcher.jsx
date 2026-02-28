import React, { useState, useRef, useEffect } from 'react';
import { LANGUAGES } from '../translations';
import { useLanguage } from '../context/LanguageContext';
import { Globe, ChevronDown } from 'lucide-react';
import './LanguageSwitcher.css';

const LanguageSwitcher = () => {
    const { lang, setLang } = useLanguage();
    const [open, setOpen] = useState(false);
    const ref = useRef(null);

    const current = LANGUAGES.find(l => l.code === lang) || LANGUAGES[0];

    // Close on outside click
    useEffect(() => {
        const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
        document.addEventListener('mousedown', handler);
        return () => document.removeEventListener('mousedown', handler);
    }, []);

    return (
        <div className="lang-dropdown-wrap" ref={ref}>
            <button className="lang-trigger" onClick={() => setOpen(o => !o)}>
                <Globe size={15} />
                <span className="lang-current">{current.nativeLabel}</span>
                <ChevronDown size={14} className={`lang-chevron ${open ? 'open' : ''}`} />
            </button>

            {open && (
                <div className="lang-menu">
                    {LANGUAGES.map(l => (
                        <button
                            key={l.code}
                            className={`lang-option ${lang === l.code ? 'active' : ''}`}
                            onClick={() => { setLang(l.code); setOpen(false); }}
                        >
                            <span className="lang-native">{l.nativeLabel}</span>
                            <span className="lang-english">{l.label}</span>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

export default LanguageSwitcher;
