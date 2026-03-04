import React, { useState, useEffect } from 'react';
import { Users, Search, Filter, Download, TrendingUp, TrendingDown, AlertCircle, CheckCircle, MapPin, Phone } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../services/api';
import './Admin.css';

const Admin = ({ onLogout }) => {
  const { t } = useLanguage();
  const [farmers, setFarmers] = useState([]);
  const [filteredFarmers, setFilteredFarmers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState('all');
  const [loading, setLoading] = useState(false);
  const [selectedFarmer, setSelectedFarmer] = useState(null);

  // Mock farmers data (in production, fetch from API)
  const mockFarmersData = [
    {
      user_id: 'rajesh_kumar_001',
      name: 'Rajesh Kumar',
      phone: '+91-9876543210',
      location: 'Pune, Maharashtra',
      gramscore: 785,
      risk_level: 'Low',
      land_acres: 3.5,
      crops: ['Rice', 'Wheat', 'Vegetables'],
      last_assessment: '2024-03-01',
      upi_consistency: 92,
      ndvi_avg: 0.72,
      loan_eligible: true,
      max_loan_amount: 200000,
    },
    {
      user_id: 'sunita_devi_002',
      name: 'Sunita Devi',
      phone: '+91-9876543211',
      location: 'Nashik, Maharashtra',
      gramscore: 625,
      risk_level: 'Medium',
      land_acres: 2.0,
      crops: ['Cotton', 'Soybean'],
      last_assessment: '2024-02-28',
      upi_consistency: 68,
      ndvi_avg: 0.58,
      loan_eligible: true,
      max_loan_amount: 100000,
    },
    {
      user_id: 'ramesh_patil_003',
      name: 'Ramesh Patil',
      phone: '+91-9876543212',
      location: 'Solapur, Maharashtra',
      gramscore: 485,
      risk_level: 'High',
      land_acres: 1.5,
      crops: ['Jowar', 'Bajra'],
      last_assessment: '2024-02-25',
      upi_consistency: 45,
      ndvi_avg: 0.42,
      loan_eligible: false,
      max_loan_amount: 50000,
    },
    {
      user_id: 'lakshmi_reddy_004',
      name: 'Lakshmi Reddy',
      phone: '+91-9876543213',
      location: 'Hyderabad, Telangana',
      gramscore: 720,
      risk_level: 'Low',
      land_acres: 4.0,
      crops: ['Rice', 'Turmeric'],
      last_assessment: '2024-03-02',
      upi_consistency: 85,
      ndvi_avg: 0.68,
      loan_eligible: true,
      max_loan_amount: 180000,
    },
    {
      user_id: 'kumar_swamy_005',
      name: 'Kumar Swamy',
      phone: '+91-9876543214',
      location: 'Bangalore, Karnataka',
      gramscore: 550,
      risk_level: 'Medium',
      land_acres: 2.5,
      crops: ['Coffee', 'Pepper'],
      last_assessment: '2024-02-20',
      upi_consistency: 58,
      ndvi_avg: 0.52,
      loan_eligible: true,
      max_loan_amount: 80000,
    },
  ];

  useEffect(() => {
    loadFarmersData();
  }, []);

  useEffect(() => {
    filterFarmers();
  }, [searchTerm, filterRisk, farmers]);

  const loadFarmersData = () => {
    setLoading(true);
    // In production, fetch from API: api.getAllFarmers()
    setTimeout(() => {
      setFarmers(mockFarmersData);
      setFilteredFarmers(mockFarmersData);
      setLoading(false);
    }, 500);
  };

  const filterFarmers = () => {
    let filtered = farmers;

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(farmer =>
        farmer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        farmer.user_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        farmer.phone.includes(searchTerm) ||
        farmer.location.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Risk filter
    if (filterRisk !== 'all') {
      filtered = filtered.filter(farmer => farmer.risk_level === filterRisk);
    }

    setFilteredFarmers(filtered);
  };

  const exportToCSV = () => {
    const headers = ['User ID', 'Name', 'Phone', 'Location', 'GramScore', 'Risk Level', 'Land (acres)', 'Crops', 'Loan Eligible', 'Max Loan'];
    const rows = filteredFarmers.map(f => [
      f.user_id,
      f.name,
      f.phone,
      f.location,
      f.gramscore,
      f.risk_level,
      f.land_acres,
      f.crops.join('; '),
      f.loan_eligible ? 'Yes' : 'No',
      f.max_loan_amount,
    ]);

    const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `gramscore_farmers_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  const getScoreColor = (score) => {
    if (score >= 700) return 'var(--success)';
    if (score >= 600) return 'var(--warning)';
    return 'var(--danger)';
  };

  const getRiskBadgeClass = (risk) => {
    if (risk === 'Low') return 'risk-badge low';
    if (risk === 'Medium') return 'risk-badge medium';
    return 'risk-badge high';
  };

  // Admin Dashboard
  return (
    <div className="admin-container container animate-fade-in">
      {/* Header */}
      <div className="admin-header">
        <div className="admin-title">
          <Users size={32} />
          <div>
            <h1>Farmers Management</h1>
            <p>Total Farmers: {filteredFarmers.length} / {farmers.length}</p>
          </div>
        </div>
        <button onClick={onLogout} className="btn-secondary">
          Logout
        </button>
      </div>

      {/* Statistics */}
      <div className="admin-stats">
        <div className="stat-card glass-panel">
          <div className="stat-icon" style={{ background: 'var(--success-soft)' }}>
            <CheckCircle size={24} color="var(--success)" />
          </div>
          <div className="stat-info">
            <div className="stat-value">{farmers.filter(f => f.risk_level === 'Low').length}</div>
            <div className="stat-label">Low Risk</div>
          </div>
        </div>
        <div className="stat-card glass-panel">
          <div className="stat-icon" style={{ background: 'var(--warning-soft)' }}>
            <AlertCircle size={24} color="var(--warning)" />
          </div>
          <div className="stat-info">
            <div className="stat-value">{farmers.filter(f => f.risk_level === 'Medium').length}</div>
            <div className="stat-label">Medium Risk</div>
          </div>
        </div>
        <div className="stat-card glass-panel">
          <div className="stat-icon" style={{ background: 'var(--danger-soft)' }}>
            <AlertCircle size={24} color="var(--danger)" />
          </div>
          <div className="stat-info">
            <div className="stat-value">{farmers.filter(f => f.risk_level === 'High').length}</div>
            <div className="stat-label">High Risk</div>
          </div>
        </div>
        <div className="stat-card glass-panel">
          <div className="stat-icon" style={{ background: 'var(--primary-soft)' }}>
            <TrendingUp size={24} color="var(--primary)" />
          </div>
          <div className="stat-info">
            <div className="stat-value">{Math.round(farmers.reduce((sum, f) => sum + f.gramscore, 0) / farmers.length)}</div>
            <div className="stat-label">Avg Score</div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="admin-filters glass-panel">
        <div className="search-box">
          <Search size={20} />
          <input
            type="text"
            placeholder="Search by name, ID, phone, or location..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="filter-group">
          <Filter size={20} />
          <select value={filterRisk} onChange={(e) => setFilterRisk(e.target.value)}>
            <option value="all">All Risk Levels</option>
            <option value="Low">Low Risk</option>
            <option value="Medium">Medium Risk</option>
            <option value="High">High Risk</option>
          </select>
        </div>
        <button onClick={exportToCSV} className="btn-secondary">
          <Download size={20} />
          Export CSV
        </button>
      </div>

      {/* Farmers Table */}
      <div className="farmers-table-container glass-panel">
        {loading ? (
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <p>Loading farmers data...</p>
          </div>
        ) : (
          <table className="farmers-table">
            <thead>
              <tr>
                <th>Farmer</th>
                <th>Contact</th>
                <th>Location</th>
                <th>GramScore</th>
                <th>Risk Level</th>
                <th>Land</th>
                <th>Crops</th>
                <th>Loan Eligible</th>
                <th>Max Loan</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredFarmers.map((farmer) => (
                <tr key={farmer.user_id} onClick={() => setSelectedFarmer(farmer)}>
                  <td>
                    <div className="farmer-name">
                      <strong>{farmer.name}</strong>
                      <span className="farmer-id">{farmer.user_id}</span>
                    </div>
                  </td>
                  <td>
                    <div className="farmer-contact">
                      <Phone size={14} />
                      {farmer.phone}
                    </div>
                  </td>
                  <td>
                    <div className="farmer-location">
                      <MapPin size={14} />
                      {farmer.location}
                    </div>
                  </td>
                  <td>
                    <div className="score-cell" style={{ color: getScoreColor(farmer.gramscore) }}>
                      <strong>{farmer.gramscore}</strong>
                      {farmer.gramscore >= 700 ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                    </div>
                  </td>
                  <td>
                    <span className={getRiskBadgeClass(farmer.risk_level)}>
                      {farmer.risk_level}
                    </span>
                  </td>
                  <td>{farmer.land_acres} acres</td>
                  <td>
                    <div className="crops-cell">
                      {farmer.crops.slice(0, 2).join(', ')}
                      {farmer.crops.length > 2 && <span className="crops-more">+{farmer.crops.length - 2}</span>}
                    </div>
                  </td>
                  <td>
                    {farmer.loan_eligible ? (
                      <span className="badge-success">Yes</span>
                    ) : (
                      <span className="badge-danger">No</span>
                    )}
                  </td>
                  <td>₹{farmer.max_loan_amount.toLocaleString()}</td>
                  <td>
                    <button className="btn-view" onClick={() => setSelectedFarmer(farmer)}>
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Farmer Detail Modal */}
      {selectedFarmer && (
        <div className="modal-overlay" onClick={() => setSelectedFarmer(null)}>
          <div className="modal-content glass-panel" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{selectedFarmer.name}</h2>
              <button onClick={() => setSelectedFarmer(null)} className="modal-close">×</button>
            </div>
            <div className="modal-body">
              <div className="detail-grid">
                <div className="detail-item">
                  <label>User ID</label>
                  <value>{selectedFarmer.user_id}</value>
                </div>
                <div className="detail-item">
                  <label>Phone</label>
                  <value>{selectedFarmer.phone}</value>
                </div>
                <div className="detail-item">
                  <label>Location</label>
                  <value>{selectedFarmer.location}</value>
                </div>
                <div className="detail-item">
                  <label>GramScore</label>
                  <value style={{ color: getScoreColor(selectedFarmer.gramscore), fontWeight: 'bold' }}>
                    {selectedFarmer.gramscore}
                  </value>
                </div>
                <div className="detail-item">
                  <label>Risk Level</label>
                  <value>
                    <span className={getRiskBadgeClass(selectedFarmer.risk_level)}>
                      {selectedFarmer.risk_level}
                    </span>
                  </value>
                </div>
                <div className="detail-item">
                  <label>Land Size</label>
                  <value>{selectedFarmer.land_acres} acres</value>
                </div>
                <div className="detail-item">
                  <label>Crops</label>
                  <value>{selectedFarmer.crops.join(', ')}</value>
                </div>
                <div className="detail-item">
                  <label>UPI Consistency</label>
                  <value>{selectedFarmer.upi_consistency}%</value>
                </div>
                <div className="detail-item">
                  <label>NDVI Average</label>
                  <value>{selectedFarmer.ndvi_avg}</value>
                </div>
                <div className="detail-item">
                  <label>Last Assessment</label>
                  <value>{new Date(selectedFarmer.last_assessment).toLocaleDateString()}</value>
                </div>
                <div className="detail-item">
                  <label>Loan Eligible</label>
                  <value>{selectedFarmer.loan_eligible ? 'Yes' : 'No'}</value>
                </div>
                <div className="detail-item">
                  <label>Max Loan Amount</label>
                  <value>₹{selectedFarmer.max_loan_amount.toLocaleString()}</value>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Admin;
