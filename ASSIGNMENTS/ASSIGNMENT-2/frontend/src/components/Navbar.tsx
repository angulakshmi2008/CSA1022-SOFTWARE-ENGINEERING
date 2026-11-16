import React from 'react';
import { UserRole } from '../types';

interface NavbarProps {
  currentUser: { username: string; role: UserRole; region_id: string };
  onSwitchUser: (username: string) => void;
  activeTab: string;
  onSelectTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentUser, onSwitchUser, activeTab, onSelectTab }) => {
  return (
    <header style={{
      backgroundColor: '#1e293b',
      color: '#ffffff',
      padding: '0.75rem 1.5rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      borderBottom: '1px solid #334155'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#38bdf8' }} />
          <h1 style={{ fontSize: '1.25rem', fontWeight: '700', letterSpacing: '-0.5px' }}>FulfillIQ</h1>
          <span style={{ fontSize: '0.75rem', background: '#334155', padding: '2px 8px', borderRadius: '4px', color: '#94a3b8' }}>CSA10 Release</span>
        </div>

        <nav style={{ display: 'flex', gap: '0.5rem' }}>
          {[
            { id: 'customer', label: 'Storefront (Customer)' },
            { id: 'picker', label: 'Warehouse (Picker)' },
            { id: 'support', label: 'Support Console' },
            { id: 'finance', label: 'Finance Reviewer' },
            { id: 'manager', label: 'Store Manager' },
            { id: 'admin', label: 'Admin Policies' },
            { id: 'scanner', label: 'Edge Scanner Sim' },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => onSelectTab(tab.id)}
              style={{
                backgroundColor: activeTab === tab.id ? '#2563eb' : 'transparent',
                color: activeTab === tab.id ? '#ffffff' : '#94a3b8',
                border: 'none',
                padding: '6px 12px',
                borderRadius: '6px',
                fontSize: '0.85rem',
                fontWeight: '500',
                transition: 'all 0.15s ease'
              }}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{ fontSize: '0.85rem', textAlign: 'right' }}>
          <div><strong>{currentUser.username}</strong> ({currentUser.role})</div>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Region: {currentUser.region_id}</div>
        </div>

        <select
          value={currentUser.username}
          onChange={(e) => onSwitchUser(e.target.value)}
          style={{
            backgroundColor: '#0f172a',
            color: '#e2e8f0',
            border: '1px solid #475569',
            padding: '6px 10px',
            borderRadius: '6px',
            fontSize: '0.8rem'
          }}
          title="Switch Simulated Actor Persona"
        >
          <option value="customer1">Demo: customer1 (Customer)</option>
          <option value="customer2">Demo: customer2 (Customer)</option>
          <option value="picker1">Demo: picker1 (Picker)</option>
          <option value="support1">Demo: support1 (Support)</option>
          <option value="finance1">Demo: finance1 (Finance)</option>
          <option value="manager1">Demo: manager1 (Manager)</option>
          <option value="admin1">Demo: admin1 (Admin)</option>
        </select>
      </div>
    </header>
  );
};
