import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, FileText, Mic, User, Users, LogOut } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import LanguageSwitcher from './LanguageSwitcher';
import './Navigation.css';

const Navigation = ({ user, onLogout }) => {
  const { t } = useLanguage();

  const navClass = ({ isActive }) => `nav-item ${isActive ? 'active' : ''}`;
  const mobileClass = ({ isActive }) => `mobile-nav-item ${isActive ? 'active' : ''}`;

  // Admin navigation
  if (user?.type === 'admin') {
    return (
      <>
        {/* Desktop Sidebar */}
        <nav className="desktop-sidebar">
          <div className="sidebar-brand">
            <div className="logo-icon">G</div>
            <h2>GramScore</h2>
          </div>

          <div className="nav-links">
            <NavLink to="/admin" className={navClass}>
              <Users size={19} />
              <span>Admin Portal</span>
            </NavLink>
          </div>

          <div className="sidebar-spacer" />

          <div className="sidebar-bottom">
            <div className="lang-row">
              <LanguageSwitcher />
            </div>

            <div className="profile-section">
              <div className="profile-avatar admin-avatar">A</div>
              <div className="profile-info">
                <span className="profile-name">{user.name}</span>
                <span className="profile-sub">Administrator</span>
              </div>
            </div>

            <button onClick={onLogout} className="logout-btn">
              <LogOut size={19} />
              <span>Logout</span>
            </button>
          </div>
        </nav>

        {/* Mobile top bar */}
        <div className="mobile-top-bar">
          <div className="mobile-brand">
            <div className="logo-icon-sm">G</div>
            <span>GramScore Admin</span>
          </div>
          <button onClick={onLogout} className="mobile-logout-btn">
            <LogOut size={20} />
          </button>
        </div>
      </>
    );
  }

  // Farmer navigation
  return (
    <>
      {/* Desktop Sidebar */}
      <nav className="desktop-sidebar">
        <div className="sidebar-brand">
          <div className="logo-icon">G</div>
          <h2>GramScore</h2>
        </div>

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

        <div className="sidebar-spacer" />

        <div className="sidebar-bottom">
          <div className="lang-row">
            <LanguageSwitcher />
          </div>

          <NavLink to="/profile" className={navClass}>
            <div className="profile-avatar">{user?.name?.charAt(0) || 'R'}</div>
            <div className="profile-info">
              <span className="profile-name">{user?.name || 'Farmer'}</span>
              <span className="profile-sub">{t.nav.profile}</span>
            </div>
          </NavLink>

          <button onClick={onLogout} className="logout-btn">
            <LogOut size={19} />
            <span>Logout</span>
          </button>
        </div>
      </nav>

      {/* Mobile top bar */}
      <div className="mobile-top-bar">
        <div className="mobile-brand">
          <div className="logo-icon-sm">G</div>
          <span>GramScore</span>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <LanguageSwitcher />
          <button onClick={onLogout} className="mobile-logout-btn">
            <LogOut size={20} />
          </button>
        </div>
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
