import React, { useState, useEffect } from 'react';
import { UserRole } from './types';
import { setAuthToken, api } from './api/client';
import { Navbar } from './components/Navbar';
import { CustomerPortal } from './pages/CustomerPortal';
import { PickerDashboard } from './pages/PickerDashboard';
import { SupportConsole } from './pages/SupportConsole';
import { FinanceConsole } from './pages/FinanceConsole';
import { ManagerDashboard } from './pages/ManagerDashboard';
import { AdminPanel } from './pages/AdminPanel';
import { ScannerSimulator } from './pages/ScannerSimulator';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('customer');
  const [currentUser, setCurrentUser] = useState<{
    username: string;
    role: UserRole;
    region_id: string;
    user_id: string;
  }>({
    username: 'customer1',
    role: 'CUSTOMER',
    region_id: 'US-EAST',
    user_id: ''
  });

  const handleLoginUser = async (username: string) => {
    try {
      // Passwords configured in database/seed_data.py
      const pwdMap: Record<string, string> = {
        customer1: 'customer123',
        customer2: 'customer123',
        picker1: 'picker123',
        support1: 'support123',
        finance1: 'finance123',
        manager1: 'manager123',
        admin1: 'admin123',
      };
      const pwd = pwdMap[username] || 'customer123';
      const res = await api.login(username, pwd);
      setAuthToken(res.access_token);
      setCurrentUser({
        username: res.username,
        role: res.role as UserRole,
        region_id: res.region_id,
        user_id: res.user_id
      });
      // Automatically switch default tab to match user persona
      if (res.role === 'PICKER') setActiveTab('picker');
      else if (res.role === 'SUPPORT_AGENT') setActiveTab('support');
      else if (res.role === 'FINANCE_REVIEWER') setActiveTab('finance');
      else if (res.role === 'STORE_MANAGER') setActiveTab('manager');
      else if (res.role === 'ADMINISTRATOR') setActiveTab('admin');
      else setActiveTab('customer');
    } catch (err: any) {
      console.error("Login failed:", err);
    }
  };

  useEffect(() => {
    handleLoginUser('customer1');
  }, []);

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar
        currentUser={currentUser}
        onSwitchUser={handleLoginUser}
        activeTab={activeTab}
        onSelectTab={setActiveTab}
      />
      <main style={{ flex: 1 }}>
        {activeTab === 'customer' && <CustomerPortal />}
        {activeTab === 'picker' && <PickerDashboard />}
        {activeTab === 'support' && <SupportConsole />}
        {activeTab === 'finance' && <FinanceConsole />}
        {activeTab === 'manager' && <ManagerDashboard />}
        {activeTab === 'admin' && <AdminPanel />}
        {activeTab === 'scanner' && <ScannerSimulator />}
      </main>
      <footer style={{ background: '#1e293b', color: '#94a3b8', padding: '1rem', textAlign: 'center', fontSize: '0.8rem', borderTop: '1px solid #334155' }}>
        FulfillIQ Omnichannel Order Fulfilment Architecture • CSA10 Software Engineering Assignment 2 • All 7 Tasks Demonstrated
      </footer>
    </div>
  );
};
