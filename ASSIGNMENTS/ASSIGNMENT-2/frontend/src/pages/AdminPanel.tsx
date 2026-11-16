import React, { useState, useEffect } from 'react';
import { RegionalPolicy } from '../types';
import { api } from '../api/client';

export const AdminPanel: React.FC = () => {
  const [policies, setPolicies] = useState<RegionalPolicy[]>([]);
  const [editingRegion, setEditingRegion] = useState<string | null>(null);
  const [taxRate, setTaxRate] = useState<number>(0);
  const [shippingFee, setShippingFee] = useState<number>(0);
  const [refundThreshold, setRefundThreshold] = useState<number>(0);
  const [message, setMessage] = useState<string | null>(null);

  const loadPolicies = async () => {
    try {
      const data = await api.getPolicies();
      setPolicies(data);
    } catch (err: any) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadPolicies();
  }, []);

  const handleStartEdit = (policy: RegionalPolicy) => {
    setEditingRegion(policy.region_id);
    setTaxRate(policy.tax_rate);
    setShippingFee(policy.shipping_fee);
    setRefundThreshold(policy.refund_approval_threshold);
  };

  const handleSavePolicy = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingRegion) return;
    try {
      const updated = await api.updatePolicy(editingRegion, {
        tax_rate: taxRate,
        shipping_fee: shippingFee,
        refund_approval_threshold: refundThreshold
      });
      setMessage(`Regional policy for ${editingRegion} updated to Version ${updated.policy_version}! Historical orders retain prior version snapshot.`);
      setEditingRegion(null);
      loadPolicies();
    } catch (err: any) {
      setMessage(`Update failed: ${err.message}`);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: '700' }}>Enterprise Policy Configuration & Governance</h2>
        <p style={{ color: '#64748b', fontSize: '0.9rem' }}>Versioned policy registry for 12 operating regions. Policy updates snapshot an immutable version number without rewriting historical transaction totals.</p>
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
              <th style={{ padding: '10px 14px' }}>Region ID</th>
              <th style={{ padding: '10px 14px' }}>Hub Name</th>
              <th style={{ padding: '10px 14px' }}>Active Policy Version</th>
              <th style={{ padding: '10px 14px' }}>Sales Tax Rate</th>
              <th style={{ padding: '10px 14px' }}>Regional Shipping Fee</th>
              <th style={{ padding: '10px 14px' }}>Refund Review Threshold</th>
              <th style={{ padding: '10px 14px' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {policies.map(p => (
              <tr key={p.region_id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '10px 14px', fontWeight: '700' }}>{p.region_id}</td>
                <td style={{ padding: '10px 14px' }}>{p.region_name}</td>
                <td style={{ padding: '10px 14px' }}>
                  <span style={{ padding: '2px 8px', borderRadius: '4px', background: '#f1f5f9', fontWeight: '700' }}>
                    v{p.policy_version}
                  </span>
                </td>
                <td style={{ padding: '10px 14px' }}>{(p.tax_rate * 100).toFixed(2)}%</td>
                <td style={{ padding: '10px 14px' }}>${p.shipping_fee.toFixed(2)}</td>
                <td style={{ padding: '10px 14px', fontWeight: '600' }}>${p.refund_approval_threshold.toFixed(2)}</td>
                <td style={{ padding: '10px 14px' }}>
                  <button
                    onClick={() => handleStartEdit(p)}
                    style={{ padding: '4px 10px', background: '#2563eb', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '600' }}
                  >
                    Edit Policy
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Edit Modal */}
      {editingRegion && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center'
        }}>
          <div style={{ background: '#ffffff', borderRadius: '8px', padding: '1.5rem', width: '450px' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '1rem' }}>Update Regional Policy: {editingRegion}</h3>
            <form onSubmit={handleSavePolicy}>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '4px' }}>Sales Tax Rate (e.g., 0.0825 = 8.25%)</label>
                <input
                  type="number" step="0.0001" min="0" max="1" required value={taxRate}
                  onChange={(e) => setTaxRate(parseFloat(e.target.value))}
                  style={{ width: '100%', padding: '6px', border: '1px solid #cbd5e1', borderRadius: '4px' }}
                />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '4px' }}>Base Shipping Fee ($)</label>
                <input
                  type="number" step="0.01" min="0" required value={shippingFee}
                  onChange={(e) => setShippingFee(parseFloat(e.target.value))}
                  style={{ width: '100%', padding: '6px', border: '1px solid #cbd5e1', borderRadius: '4px' }}
                />
              </div>
              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '4px' }}>Refund Dual-Control Approval Threshold ($)</label>
                <input
                  type="number" step="0.01" min="0" required value={refundThreshold}
                  onChange={(e) => setRefundThreshold(parseFloat(e.target.value))}
                  style={{ width: '100%', padding: '6px', border: '1px solid #cbd5e1', borderRadius: '4px' }}
                />
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
                <button type="button" onClick={() => setEditingRegion(null)} style={{ padding: '6px 12px', background: '#e2e8f0', border: 'none', borderRadius: '4px' }}>Cancel</button>
                <button type="submit" style={{ padding: '6px 12px', background: '#2563eb', color: '#fff', border: 'none', borderRadius: '4px', fontWeight: '600' }}>Save Versioned Policy</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
