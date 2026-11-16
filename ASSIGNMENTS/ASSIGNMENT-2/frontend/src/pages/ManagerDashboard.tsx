import React, { useState, useEffect } from 'react';
import { api } from '../api/client';

export const ManagerDashboard: React.FC = () => {
  const [summary, setSummary] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  const loadSummary = async () => {
    setLoading(true);
    try {
      const data = await api.getReportSummary();
      setSummary(data);
    } catch (err: any) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSummary();
  }, []);

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: '700' }}>Store Manager & Executive Analytics</h2>
          <p style={{ color: '#64748b', fontSize: '0.9rem' }}>Consolidated cross-regional reporting served from read-only summary models to prevent database lock contention.</p>
        </div>
        <button
          onClick={loadSummary}
          style={{ padding: '8px 16px', background: '#2563eb', color: '#fff', border: 'none', borderRadius: '6px', fontWeight: '600' }}
        >
          {loading ? 'Refreshing...' : 'Refresh Reports'}
        </button>
      </div>

      {summary && (
        <>
          {/* KPI Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem', marginBottom: '2rem' }}>
            <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.25rem' }}>
              <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: '600', textTransform: 'uppercase' }}>Gross Revenue</div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: '#16a34a', marginTop: '0.25rem' }}>
                ${(summary.sales_summary?.gross_revenue || 0).toFixed(2)}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '4px' }}>From {summary.sales_summary?.total_orders || 0} Paid Orders</div>
            </div>

            <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.25rem' }}>
              <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: '600', textTransform: 'uppercase' }}>Regional Tax Collected</div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: '#0f172a', marginTop: '0.25rem' }}>
                ${(summary.sales_summary?.total_tax_collected || 0).toFixed(2)}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '4px' }}>Across 12 Global Jurisdictions</div>
            </div>

            <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.25rem' }}>
              <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: '600', textTransform: 'uppercase' }}>Available Warehouse Inventory</div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: '#2563eb', marginTop: '0.25rem' }}>
                {summary.inventory_summary?.total_available || 0} Units
              </div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '4px' }}>
                {summary.inventory_summary?.total_on_hand || 0} On Hand / {summary.inventory_summary?.total_reserved || 0} Reserved
              </div>
            </div>

            <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.25rem' }}>
              <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: '600', textTransform: 'uppercase' }}>Active Refunds</div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: '#dc2626', marginTop: '0.25rem' }}>
                {summary.refunds_summary?.reduce((acc: number, r: any) => acc + r.count, 0) || 0}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '4px' }}>Requested, Approved or Failed</div>
            </div>
          </div>

          {/* Regional Breakdown Table */}
          <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.5rem', marginBottom: '2rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '1rem' }}>Regional Sales Performance (12 Operating Hubs)</h3>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
              <thead>
                <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', color: '#475569' }}>
                  <th style={{ padding: '8px 12px' }}>Region Hub</th>
                  <th style={{ padding: '8px 12px' }}>Completed Orders</th>
                  <th style={{ padding: '8px 12px' }}>Regional Revenue ($)</th>
                </tr>
              </thead>
              <tbody>
                {summary.regional_breakdown?.length === 0 ? (
                  <tr><td colSpan={3} style={{ padding: '1rem', color: '#64748b' }}>No regional transactions recorded yet.</td></tr>
                ) : (
                  summary.regional_breakdown?.map((reg: any) => (
                    <tr key={reg.region_id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                      <td style={{ padding: '8px 12px', fontWeight: '600' }}>{reg.region_id}</td>
                      <td style={{ padding: '8px 12px' }}>{reg.order_count}</td>
                      <td style={{ padding: '8px 12px', fontWeight: '700', color: '#16a34a' }}>${reg.regional_revenue.toFixed(2)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
};
