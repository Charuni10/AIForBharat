import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, FileText, Mic, User } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import LanguageSwitcher from './LanguageSwitcher';
import './Navigation.css';

const Navigation = () => {
  const { t } = useLanguage();

  const navClass = ({ isActive }) => `nav-item ${isActive ? 'active' : ''}`;
  const mobileClass = ({ isActive }) => `mobile-nav-item ${isActive ? 'active' : ''}`;

  return (
    <>
      {/* Desktop Sidebar */}
      <nav className="desktop-sidebar">
        {/* Brand at top */}
        <div className="sidebar-brand">
          <div className="logo-icon">G</div>
          <h2>GramScore</h2>
        </div>

        {/* Nav links */}
        <div className="nav-links">
          <NavLink to="/" className={navClass} end>
            <Home size={19} />
            <span>{t.nav.dashboard}</span>
          </NavLink>
          <NavLink to="/consent" className={navClass}>
            <FileText size={19} />
            <span>{t.nav.approvals}</span>
          </NavLink>
          <NavLink to="/assessment" className={navClass}>
            <Mic size={19} />
            <span>{t.nav.assessment}</span>
          </NavLink>
        </div>

        {/* Spacer pushes bottom section down */}
        <div className="sidebar-spacer" />

        {/* Bottom: Profile + Language */}
        <div className="sidebar-bottom">
          <div className="lang-row">
            <LanguageSwitcher />
          </div>

          <NavLink to="/profile" className={navClass}>
            <div className="profile-avatar">R</div>
            <div className="profile-info">
              <span className="profile-name">Rajesh Kumar</span>
              <span className="profile-sub">{t.nav.profile}</span>
            </div>
          </NavLink>
        </div>
      </nav>

      {/* Mobile top bar */}
      <div className="mobile-top-bar">
        <div className="mobile-brand">
          <div className="logo-icon-sm">G</div>
          <span>GramScore</span>
        </div>
        <LanguageSwitcher />
      </div>

      {/* Mobile Bottom Bar */}
      <nav className="mobile-bottom-bar">
        <NavLink to="/" className={mobileClass} end>
          <Home size={22} />
          <span>{t.nav.dashboard}</span>
        </NavLink>
        <NavLink to="/consent" className={mobileClass}>
          <FileText size={22} />
          <span>{t.nav.approvals}</span>
        </NavLink>
        <NavLink to="/assessment" className={mobileClass}>
          <Mic size={22} />
          <span>{t.nav.assessment}</span>
        </NavLink>
        <NavLink to="/profile" className={mobileClass}>
          <User size={22} />
          <span>{t.nav.profile}</span>
        </NavLink>
      </nav>
    </>
  );
};

export default Navigation;
