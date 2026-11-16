import React, { useState, useEffect } from 'react';
import { RefundRequest } from '../types';
import { api } from '../api/client';

export const FinanceConsole: React.FC = () => {
  const [refunds, setRefunds] = useState<RefundRequest[]>([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [simulateFail, setSimulateFail] = useState(false);

  const loadRefunds = async () => {
    try {
      const data = await api.getRefunds();
      setRefunds(data);
    } catch (err: any) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadRefunds();
  }, []);

  const handleDecision = async (refundId: string, decision: 'APPROVE' | 'REJECT') => {
    setLoading(true);
    try {
      await api.decideRefund(refundId, decision, `Finance officer reviewed return evidence: ${decision}`);
      setMessage(`Refund ${refundId} marked as ${decision}D!`);
      loadRefunds();
    } catch (err: any) {
      setMessage(`Decision failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleExecute = async (refundId: string) => {
    setLoading(true);
    try {
      const res = await api.executeRefund(refundId, simulateFail);
      if (res.state === 'FAILED') {
        setMessage(`Gateway execution simulated failure! Approval retained for safe retry: ${res.failure_reason}`);
      } else {
        setMessage(`Refund ${refundId} successfully EXECUTED with gateway! Customer credited.`);
      }
      loadRefunds();
    } catch (err: any) {
      setMessage(`Execution failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: '700' }}>Finance Reviewer & Refund Governance</h2>
          <p style={{ color: '#64748b', fontSize: '0.9rem' }}>Dual-control refund authorizations. Amounts exceeding $50.00 require human finance review. Failed gateway execution retains approval.</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', background: '#ffffff', padding: '6px 12px', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
          <label style={{ fontSize: '0.85rem', fontWeight: '600', color: simulateFail ? '#dc2626' : '#475569' }}>
            Simulate Gateway Failure on Execute:
          </label>
          <input
            type="checkbox"
            checked={simulateFail}
            onChange={(e) => setSimulateFail(e.target.checked)}
            style={{ width: '16px', height: '16px' }}
          />
        </div>
      </div>

      {message && (
        <div style={{ padding: '1rem', borderRadius: '6px', marginBottom: '1rem', background: '#f0fdf4', color: '#15803d', border: '1px solid #bbf7d0' }}>
          {message}
        </div>
      )}

      <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', color: '#475569' }}>
              <th style={{ padding: '10px 14px' }}>Refund ID</th>
              <th style={{ padding: '10px 14px' }}>Order ID</th>
              <th style={{ padding: '10px 14px' }}>Amount</th>
              <th style={{ padding: '10px 14px' }}>Threshold Policy</th>
              <th style={{ padding: '10px 14px' }}>State</th>
              <th style={{ padding: '10px 14px' }}>Approved By</th>
              <th style={{ padding: '10px 14px' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {refunds.length === 0 ? (
              <tr>
                <td colSpan={7} style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>No refund requests queued.</td>
              </tr>
            ) : (
              refunds.map(r => (
                <tr key={r.refund_id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                  <td style={{ padding: '10px 14px', fontFamily: 'monospace' }}>{r.refund_id.slice(0, 8)}...</td>
                  <td style={{ padding: '10px 14px', fontFamily: 'monospace' }}>{r.order_id.slice(0, 8)}...</td>
                  <td style={{ padding: '10px 14px', fontWeight: '700' }}>${r.amount.toFixed(2)}</td>
                  <td style={{ padding: '10px 14px' }}>
                    <span style={{
                      padding: '2px 6px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '600',
                      background: r.amount > 50 ? '#fee2e2' : '#dcfce7',
                      color: r.amount > 50 ? '#991b1b' : '#166534'
                    }}>
                      {r.amount > 50 ? 'Dual-Control Mandatory (> $50)' : 'Policy Eligible'}
                    </span>
                  </td>
                  <td style={{ padding: '10px 14px' }}>
                    <span style={{
                      padding: '3px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '700',
                      background: r.state === 'APPROVED' ? '#dcfce7' : r.state === 'EXECUTED' ? '#e0e7ff' : r.state === 'FAILED' ? '#fee2e2' : '#fef3c7',
                      color: r.state === 'APPROVED' ? '#15803d' : r.state === 'EXECUTED' ? '#4338ca' : r.state === 'FAILED' ? '#991b1b' : '#b45309'
                    }}>
                      {r.state}
                    </span>
                    {r.failure_reason && (
                      <div style={{ fontSize: '0.75rem', color: '#dc2626', marginTop: '2px' }}>{r.failure_reason}</div>
                    )}
                  </td>
                  <td style={{ padding: '10px 14px', color: '#64748b', fontSize: '0.8rem' }}>
                    {r.approved_by ? `${r.approved_by.slice(0, 8)}...` : 'Unapproved'}
                  </td>
                  <td style={{ padding: '10px 14px' }}>
                    {r.state === 'REQUESTED' && (
                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        <button
                          disabled={loading}
                          onClick={() => handleDecision(r.refund_id, 'APPROVE')}
                          style={{ padding: '4px 8px', background: '#16a34a', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '600' }}
                        >
                          Approve
                        </button>
                        <button
                          disabled={loading}
                          onClick={() => handleDecision(r.refund_id, 'REJECT')}
                          style={{ padding: '4px 8px', background: '#dc2626', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '0.75rem' }}
                        >
                          Reject
                        </button>
                      </div>
                    )}
                    {['APPROVED', 'FAILED'].includes(r.state) && (
                      <button
                        disabled={loading}
                        onClick={() => handleExecute(r.refund_id)}
                        style={{
                          padding: '4px 10px',
                          background: r.state === 'FAILED' ? '#d97706' : '#2563eb',
                          color: '#fff', border: 'none', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '600'
                        }}
                      >
                        {r.state === 'FAILED' ? 'Controlled Retry' : 'Execute Gateway Refund'}
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
