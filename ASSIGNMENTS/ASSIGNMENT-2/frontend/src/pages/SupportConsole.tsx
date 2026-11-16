import React, { useState } from 'react';
import { api } from '../api/client';

export const SupportConsole: React.FC = () => {
  const [searchOrderId, setSearchOrderId] = useState('');
  const [order, setOrder] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [returnSuccess, setReturnSuccess] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setOrder(null);
    setReturnSuccess(null);
    try {
      const data = await api.getOrder(searchOrderId.trim());
      setOrder(data);
    } catch (err: any) {
      setError(err.message || 'Order not found');
    }
  };

  const handleInitiateReturn = async () => {
    if (!order) return;
    try {
      await api.requestRefund(order.order_id, order.total_amount, 'Customer support initiated return');
      setReturnSuccess(`Return request created for Order ${order.order_id}. Queued for Finance review.`);
    } catch (err: any) {
      setError(`Return creation failed: ${err.message}`);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: '700' }}>Customer Support Console</h2>
        <p style={{ color: '#64748b', fontSize: '0.9rem' }}>Look up order statuses, tracking tokens, and initiate return requests. Sensitive card numbers are redacted at the API boundary.</p>
      </div>

      <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem' }}>
        <input
          type="text"
          value={searchOrderId}
          onChange={(e) => setSearchOrderId(e.target.value)}
          placeholder="Enter full or partial Order UUID..."
          required
          style={{ flex: 1, padding: '10px 14px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.9rem' }}
        />
        <button
          type="submit"
          style={{ padding: '10px 20px', background: '#2563eb', color: '#fff', border: 'none', borderRadius: '6px', fontWeight: '600' }}
        >
          Lookup Order
        </button>
      </form>

      {error && (
        <div style={{ padding: '1rem', borderRadius: '6px', marginBottom: '1.5rem', background: '#fee2e2', color: '#991b1b', border: '1px solid #fca5a5' }}>
          {error}
        </div>
      )}

      {returnSuccess && (
        <div style={{ padding: '1rem', borderRadius: '6px', marginBottom: '1.5rem', background: '#dcfce7', color: '#166534', border: '1px solid #86efac' }}>
          {returnSuccess}
        </div>
      )}

      {order && (
        <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #e2e8f0', paddingBottom: '1rem', marginBottom: '1rem' }}>
            <div>
              <h3 style={{ fontSize: '1.2rem', fontWeight: '700' }}>Order Details</h3>
              <p style={{ color: '#64748b', fontSize: '0.85rem' }}>Order UUID: <code>{order.order_id}</code></p>
            </div>
            <span style={{
              padding: '4px 10px', borderRadius: '6px', fontWeight: '700', fontSize: '0.85rem',
              background: order.state === 'PAID' ? '#dcfce7' : order.state === 'DISPATCHED' ? '#e0e7ff' : '#f1f5f9',
              color: order.state === 'PAID' ? '#15803d' : order.state === 'DISPATCHED' ? '#4338ca' : '#0f172a'
            }}>
              {order.state}
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginBottom: '1.5rem', fontSize: '0.85rem' }}>
            <div><strong>Customer Owner:</strong><br /><span style={{ color: '#64748b' }}>{order.owner_id}</span></div>
            <div><strong>Region / Tax Hub:</strong><br /><span>{order.region_id} (Policy v{order.policy_version})</span></div>
            <div><strong>Payment Data:</strong><br /><span style={{ color: '#16a34a' }}>Tokenized (PAN/CVV Masked)</span></div>
            <div><strong>Subtotal:</strong><br />${order.subtotal.toFixed(2)}</div>
            <div><strong>Regional Tax:</strong><br />${order.tax_amount.toFixed(2)}</div>
            <div><strong>Order Grand Total:</strong><br /><strong style={{ fontSize: '1rem', color: '#2563eb' }}>${order.total_amount.toFixed(2)}</strong></div>
          </div>

          <h4 style={{ fontSize: '0.95rem', fontWeight: '600', marginBottom: '0.5rem' }}>Order Items</h4>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem', marginBottom: '1.5rem' }}>
            <thead>
              <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', textAlign: 'left' }}>
                <th style={{ padding: '8px' }}>SKU</th>
                <th style={{ padding: '8px' }}>Quantity</th>
                <th style={{ padding: '8px' }}>Unit Price</th>
                <th style={{ padding: '8px' }}>Line Total</th>
              </tr>
            </thead>
            <tbody>
              {order.items?.map((it: any) => (
                <tr key={it.line_id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                  <td style={{ padding: '8px', fontWeight: '600' }}>{it.sku}</td>
                  <td style={{ padding: '8px' }}>{it.quantity}</td>
                  <td style={{ padding: '8px' }}>${it.unit_price.toFixed(2)}</td>
                  <td style={{ padding: '8px', fontWeight: '600' }}>${it.line_total.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
            <button
              onClick={handleInitiateReturn}
              style={{
                padding: '8px 16px', background: '#e0f2fe', color: '#0369a1',
                border: '1px solid #bae6fd', borderRadius: '6px', fontWeight: '600', fontSize: '0.85rem'
              }}
            >
              Initiate Customer Return
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
