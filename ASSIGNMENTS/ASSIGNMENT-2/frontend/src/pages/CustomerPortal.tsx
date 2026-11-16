import React, { useState, useEffect } from 'react';
import { Product, Order } from '../types';
import { api } from '../api/client';

export const CustomerPortal: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [cart, setCart] = useState<{ [sku: string]: number }>({});
  const [selectedRegion, setSelectedRegion] = useState('US-EAST');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  // Return modal state
  const [returnOrderId, setReturnOrderId] = useState<string | null>(null);
  const [returnAmount, setReturnAmount] = useState<number>(0);
  const [returnReason, setReturnReason] = useState<string>('');

  const loadData = async () => {
    try {
      const [prods, ords] = await Promise.all([
        api.getProducts(selectedRegion),
        api.getOrders()
      ]);
      setProducts(prods);
      setOrders(ords);
    } catch (err: any) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedRegion]);

  const addToCart = (sku: string) => {
    setCart(prev => ({ ...prev, [sku]: (prev[sku] || 0) + 1 }));
  };

  const removeFromCart = (sku: string) => {
    setCart(prev => {
      const next = { ...prev };
      delete next[sku];
      return next;
    });
  };

  const handleCheckout = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const items = Object.entries(cart).map(([sku, qty]) => ({ sku, quantity: qty }));
      const order = await api.placeOrder(items, selectedRegion);
      setMessage({ text: `Order ${order.order_id} placed successfully! State: ${order.state}. Total: $${order.total_amount}`, type: 'success' });
      setCart({});
      loadData();
    } catch (err: any) {
      setMessage({ text: `Checkout failed: ${err.message}`, type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleSimulatePayment = async (order: Order) => {
    setLoading(true);
    try {
      // Create signed mock callback payload
      const payload = {
        gateway_id: "STRIPE_SANDBOX",
        event_id: `evt_ui_${Date.now()}`,
        order_id: order.order_id,
        amount: order.total_amount,
        currency: "USD",
        status: "CAPTURED"
      };
      
      // Calculate signature client-side for demo webhook trigger
      // Using pre-shared key "webhook-secret-hmac-sha256-key"
      const encoder = new TextEncoder();
      const keyData = encoder.encode("webhook-secret-hmac-sha256-key");
      const key = await window.crypto.subtle.importKey(
        "raw", keyData, { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
      );
      const signatureBuffer = await window.crypto.subtle.sign(
        "HMAC", key, encoder.encode(JSON.stringify(payload, Object.keys(payload).sort()))
      );
      const signatureHex = Array.from(new Uint8Array(signatureBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');

      await api.submitPaymentCallback(payload, signatureHex);
      setMessage({ text: `Payment confirmed for order ${order.order_id}! Outbox intent enqueued.`, type: 'success' });
      loadData();
    } catch (err: any) {
      setMessage({ text: `Payment webhook failed: ${err.message}`, type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleRequestReturn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!returnOrderId) return;
    try {
      await api.requestRefund(returnOrderId, returnAmount, returnReason);
      setMessage({ text: `Return request submitted for order ${returnOrderId}. Awaiting finance review.`, type: 'success' });
      setReturnOrderId(null);
      loadData();
    } catch (err: any) {
      setMessage({ text: `Return submission failed: ${err.message}`, type: 'error' });
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: '700' }}>Customer Storefront & Orders</h2>
          <p style={{ color: '#64748b', fontSize: '0.9rem' }}>Browse catalogue with atomic reservation and server-calculated regional tax.</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <label style={{ fontSize: '0.85rem', fontWeight: '600' }}>Select Delivery Region:</label>
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            style={{ padding: '6px 12px', borderRadius: '6px', border: '1px solid #cbd5e1' }}
          >
            {['US-EAST', 'US-WEST', 'US-CENTRAL', 'CAN-EAST', 'UK-SOUTH', 'EU-CENTRAL', 'EU-WEST', 'APAC-EAST', 'APAC-SOUTH', 'AUS-EAST', 'LATAM-BR', 'MEA-UAE'].map(r => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>
      </div>

      {message && (
        <div style={{
          padding: '1rem',
          borderRadius: '6px',
          marginBottom: '1.5rem',
          backgroundColor: message.type === 'success' ? '#dcfce7' : '#fee2e2',
          color: message.type === 'success' ? '#166534' : '#991b1b',
          border: `1px solid ${message.type === 'success' ? '#86efac' : '#fca5a5'}`
        }}>
          {message.text}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
        {/* Products Grid */}
        <div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '1rem' }}>Available Products</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '1rem' }}>
            {products.map(p => (
              <div key={p.sku} style={{
                background: '#ffffff',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                padding: '1rem',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: '600', textTransform: 'uppercase' }}>{p.category}</div>
                  <h4 style={{ fontSize: '1rem', fontWeight: '600', margin: '0.25rem 0' }}>{p.name}</h4>
                  <p style={{ fontSize: '0.8rem', color: '#475569', marginBottom: '0.75rem' }}>{p.description}</p>
                </div>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                    <span style={{ fontSize: '1.1rem', fontWeight: '700', color: '#0f172a' }}>${p.base_price.toFixed(2)}</span>
                    <span style={{
                      fontSize: '0.75rem',
                      padding: '2px 6px',
                      borderRadius: '4px',
                      background: p.available_stock > 0 ? '#e0f2fe' : '#fee2e2',
                      color: p.available_stock > 0 ? '#0369a1' : '#991b1b',
                      fontWeight: '600'
                    }}>
                      {p.available_stock > 0 ? `${p.available_stock} Available` : 'Out of Stock'}
                    </span>
                  </div>
                  <button
                    disabled={p.available_stock <= 0}
                    onClick={() => addToCart(p.sku)}
                    style={{
                      width: '100%',
                      padding: '8px',
                      borderRadius: '6px',
                      border: 'none',
                      backgroundColor: p.available_stock > 0 ? '#2563eb' : '#94a3b8',
                      color: '#ffffff',
                      fontWeight: '600',
                      fontSize: '0.85rem'
                    }}
                  >
                    {p.available_stock > 0 ? 'Add to Cart' : 'Sold Out'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Cart Sidebar */}
        <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.25rem', height: 'fit-content' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '1rem' }}>Your Shopping Cart</h3>
          {Object.keys(cart).length === 0 ? (
            <p style={{ color: '#64748b', fontSize: '0.9rem' }}>Your cart is empty.</p>
          ) : (
            <div>
              {Object.entries(cart).map(([sku, qty]) => {
                const prod = products.find(p => p.sku === sku);
                return (
                  <div key={sku} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', fontSize: '0.85rem' }}>
                    <div>
                      <div><strong>{prod?.name || sku}</strong></div>
                      <div style={{ color: '#64748b' }}>Qty: {qty} × ${prod?.base_price.toFixed(2)}</div>
                    </div>
                    <button
                      onClick={() => removeFromCart(sku)}
                      style={{ background: 'transparent', border: 'none', color: '#dc2626', fontSize: '0.8rem' }}
                    >
                      Remove
                    </button>
                  </div>
                );
              })}
              <div style={{ borderTop: '1px solid #e2e8f0', paddingTop: '1rem', marginTop: '1rem' }}>
                <p style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '0.75rem' }}>
                  * Final taxes and shipping will be authoritatively calculated by the server for <strong>{selectedRegion}</strong>.
                </p>
                <button
                  disabled={loading}
                  onClick={handleCheckout}
                  style={{
                    width: '100%',
                    padding: '10px',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor: '#16a34a',
                    color: '#ffffff',
                    fontWeight: '700',
                    fontSize: '0.95rem'
                  }}
                >
                  {loading ? 'Processing...' : 'Checkout (Reserve Stock)'}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Orders Table */}
      <div style={{ marginTop: '3rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: '600', marginBottom: '1rem' }}>Your Orders & Tracking</h3>
        <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', color: '#475569' }}>
                <th style={{ padding: '10px 14px' }}>Order ID</th>
                <th style={{ padding: '10px 14px' }}>Region</th>
                <th style={{ padding: '10px 14px' }}>Status</th>
                <th style={{ padding: '10px 14px' }}>Total Amount</th>
                <th style={{ padding: '10px 14px' }}>Placed At</th>
                <th style={{ padding: '10px 14px' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.length === 0 ? (
                <tr>
                  <td colSpan={6} style={{ padding: '1.5rem', textAlign: 'center', color: '#64748b' }}>No orders found.</td>
                </tr>
              ) : (
                orders.map(o => (
                  <tr key={o.order_id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '10px 14px', fontFamily: 'monospace' }}>{o.order_id.slice(0, 8)}...</td>
                    <td style={{ padding: '10px 14px' }}>{o.region_id}</td>
                    <td style={{ padding: '10px 14px' }}>
                      <span style={{
                        padding: '3px 8px',
                        borderRadius: '4px',
                        fontSize: '0.75rem',
                        fontWeight: '700',
                        background: o.state === 'PAID' ? '#dcfce7' : o.state === 'DISPATCHED' ? '#e0e7ff' : o.state === 'PLACED' ? '#fef3c7' : '#f1f5f9',
                        color: o.state === 'PAID' ? '#15803d' : o.state === 'DISPATCHED' ? '#4338ca' : o.state === 'PLACED' ? '#b45309' : '#334155'
                      }}>
                        {o.state}
                      </span>
                    </td>
                    <td style={{ padding: '10px 14px', fontWeight: '600' }}>${o.total_amount.toFixed(2)}</td>
                    <td style={{ padding: '10px 14px', color: '#64748b' }}>{o.created_at}</td>
                    <td style={{ padding: '10px 14px' }}>
                      {o.state === 'PLACED' && (
                        <button
                          onClick={() => handleSimulatePayment(o)}
                          style={{
                            padding: '4px 8px',
                            background: '#2563eb',
                            color: '#fff',
                            border: 'none',
                            borderRadius: '4px',
                            fontSize: '0.75rem',
                            fontWeight: '600',
                            marginRight: '6px'
                          }}
                        >
                          Simulate Gateway Payment
                        </button>
                      )}
                      {['PAID', 'PACKED', 'DISPATCHED', 'DELIVERED'].includes(o.state) && (
                        <button
                          onClick={() => {
                            setReturnOrderId(o.order_id);
                            setReturnAmount(o.total_amount);
                          }}
                          style={{
                            padding: '4px 8px',
                            background: '#f8fafc',
                            color: '#0f172a',
                            border: '1px solid #cbd5e1',
                            borderRadius: '4px',
                            fontSize: '0.75rem'
                          }}
                        >
                          Request Return
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

      {/* Return Request Modal */}
      {returnOrderId && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center'
        }}>
          <div style={{ background: '#ffffff', borderRadius: '8px', padding: '1.5rem', width: '400px' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '1rem' }}>Request Order Return / Refund</h3>
            <form onSubmit={handleRequestReturn}>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '4px' }}>Order ID</label>
                <input type="text" readOnly value={returnOrderId} style={{ width: '100%', padding: '6px', background: '#f8fafc', border: '1px solid #cbd5e1', borderRadius: '4px' }} />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '4px' }}>Refund Amount ($)</label>
                <input
                  type="number" step="0.01" value={returnAmount}
                  onChange={(e) => setReturnAmount(parseFloat(e.target.value))}
                  style={{ width: '100%', padding: '6px', border: '1px solid #cbd5e1', borderRadius: '4px' }}
                />
              </div>
              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '4px' }}>Reason for Return</label>
                <textarea
                  required value={returnReason}
                  onChange={(e) => setReturnReason(e.target.value)}
                  placeholder="e.g., Defective unit, incorrect size..."
                  style={{ width: '100%', padding: '6px', border: '1px solid #cbd5e1', borderRadius: '4px', minHeight: '60px' }}
                />
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
                <button type="button" onClick={() => setReturnOrderId(null)} style={{ padding: '6px 12px', background: '#e2e8f0', border: 'none', borderRadius: '4px' }}>Cancel</button>
                <button type="submit" style={{ padding: '6px 12px', background: '#2563eb', color: '#fff', border: 'none', borderRadius: '4px', fontWeight: '600' }}>Submit Return</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
