import React, { useState, useEffect } from 'react';
import { api } from '../api/client';

export const PickerDashboard: React.FC = () => {
  const [pickOrders, setPickOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const loadPickLists = async () => {
    try {
      const data = await api.getPickLists();
      setPickOrders(data);
    } catch (err: any) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadPickLists();
  }, []);

  const handlePack = async (orderId: string) => {
    setLoading(true);
    try {
      await api.packOrder(orderId);
      setMessage(`Order ${orderId} successfully picked & packed! State changed to PACKED.`);
      loadPickLists();
    } catch (err: any) {
      setMessage(`Packing failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDispatch = async (orderId: string) => {
    setLoading(true);
    try {
      await api.dispatchOrder(orderId);
      setMessage(`Order ${orderId} successfully handed over to carrier! State changed to DISPATCHED.`);
      loadPickLists();
    } catch (err: any) {
      setMessage(`Dispatch failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: '700' }}>Warehouse Picking & Packing Terminal</h2>
        <p style={{ color: '#64748b', fontSize: '0.9rem' }}>Pick lists isolated by assigned warehouse zone. Dispatch requires confirmed pick and verified payment.</p>
      </div>

      {message && (
        <div style={{ padding: '1rem', borderRadius: '6px', marginBottom: '1rem', background: '#dcfce7', color: '#166534', border: '1px solid #86efac' }}>
          {message}
        </div>
      )}

      <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', color: '#475569' }}>
              <th style={{ padding: '10px 14px' }}>Order ID</th>
              <th style={{ padding: '10px 14px' }}>Region Hub</th>
              <th style={{ padding: '10px 14px' }}>Items to Retrieve</th>
              <th style={{ padding: '10px 14px' }}>State</th>
              <th style={{ padding: '10px 14px' }}>Dispatch Due (UTC SLA)</th>
              <th style={{ padding: '10px 14px' }}>Warehouse Actions</th>
            </tr>
          </thead>
          <tbody>
            {pickOrders.length === 0 ? (
              <tr>
                <td colSpan={6} style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>
                  No pending paid orders in your assigned region. All pick lists clear!
                </td>
              </tr>
            ) : (
              pickOrders.map(o => (
                <tr key={o.order_id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                  <td style={{ padding: '10px 14px', fontFamily: 'monospace' }}>{o.order_id.slice(0, 8)}...</td>
                  <td style={{ padding: '10px 14px' }}><strong>{o.region_id}</strong></td>
                  <td style={{ padding: '10px 14px' }}>
                    {o.items?.map((it: any) => (
                      <div key={it.sku} style={{ fontSize: '0.8rem' }}>
                        • <strong>{it.sku}</strong> (Qty: {it.quantity})
                      </div>
                    ))}
                  </td>
                  <td style={{ padding: '10px 14px' }}>
                    <span style={{
                      padding: '3px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '700',
                      background: o.state === 'PAID' ? '#dcfce7' : o.state === 'PACKED' ? '#e0e7ff' : '#f1f5f9',
                      color: o.state === 'PAID' ? '#15803d' : o.state === 'PACKED' ? '#4338ca' : '#334155'
                    }}>
                      {o.state}
                    </span>
                  </td>
                  <td style={{ padding: '10px 14px', color: '#dc2626', fontWeight: '600' }}>
                    {o.dispatch_due_at || 'Pending'}
                  </td>
                  <td style={{ padding: '10px 14px' }}>
                    {o.state === 'PAID' && (
                      <button
                        disabled={loading}
                        onClick={() => handlePack(o.order_id)}
                        style={{
                          padding: '6px 12px', background: '#2563eb', color: '#fff',
                          border: 'none', borderRadius: '4px', fontWeight: '600', fontSize: '0.8rem'
                        }}
                      >
                        Confirm Pick & Pack
                      </button>
                    )}
                    {o.state === 'PACKED' && (
                      <button
                        disabled={loading}
                        onClick={() => handleDispatch(o.order_id)}
                        style={{
                          padding: '6px 12px', background: '#16a34a', color: '#fff',
                          border: 'none', borderRadius: '4px', fontWeight: '600', fontSize: '0.8rem'
                        }}
                      >
                        Handover & Dispatch
                      </button>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
