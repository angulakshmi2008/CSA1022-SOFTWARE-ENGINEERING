import React, { useState } from 'react';
import { api } from '../api/client';

export const ScannerSimulator: React.FC = () => {
  const [nodeId, setNodeId] = useState('SCANNER-WH-A1');
  const [isOnline, setIsOnline] = useState(true);
  const [offlineBuffer, setOfflineBuffer] = useState<any[]>([]);
  const [syncResult, setSyncResult] = useState<any | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  // New scan input
  const [sku, setSku] = useState('SKU-LAPTOP-001');
  const [qty, setQty] = useState(10);
  const [region, setRegion] = useState('US-EAST');

  const handleCaptureScan = () => {
    if (offlineBuffer.length >= 5000) {
      alert("BUFFER EXHAUSTION WARNING: Handheld terminal queue reached 5,000 events. Sync required!");
      return;
    }

    const newEvent = {
      node_id: nodeId,
      event_id: `scan-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      sku,
      region_id: region,
      event_type: 'RECEIVE',
      quantity: qty,
      observation_time: new Date().toISOString(),
      schema_version: '1.0'
    };

    setOfflineBuffer(prev => [...prev, newEvent]);
    setMessage(`Captured scan event ${newEvent.event_id} for ${qty}x ${sku}. (Queue depth: ${offlineBuffer.length + 1})`);
  };

  const handleSimulateDuplicate = () => {
    if (offlineBuffer.length === 0) {
      alert("Add at least one scan to buffer first!");
      return;
    }
    // Duplicate the last scan in buffer to test replay deduplication
    const lastEvent = offlineBuffer[offlineBuffer.length - 1];
    setOfflineBuffer(prev => [...prev, lastEvent]);
    setMessage(`Duplicated event ${lastEvent.event_id} in queue to test server deduplication.`);
  };

  const handleSyncBatch = async () => {
    if (!isOnline) {
      alert("Scanner is currently offline. Toggle WiFi back online to sync with server.");
      return;
    }
    if (offlineBuffer.length === 0) {
      setMessage("Offline buffer is empty. Capture scans first.");
      return;
    }

    try {
      const res = await api.syncScannerBatch(offlineBuffer);
      setSyncResult(res);
      setOfflineBuffer([]);
      setMessage(`Sync successful: Ingested ${res.received_count} scans. Processed: ${res.processed_count}, Duplicates safely ignored: ${res.duplicate_count}`);
    } catch (err: any) {
      setMessage(`Sync error: ${err.message}`);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: '700' }}>Edge Warehouse Scanner Simulation</h2>
          <p style={{ color: '#64748b', fontSize: '0.9rem' }}>Simulates intermittently disconnected handheld scanners, bounded local FIFO queues, and server deduplication.</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', background: '#ffffff', padding: '6px 14px', borderRadius: '6px', border: '1px solid #cbd5e1' }}>
          <label style={{ fontSize: '0.85rem', fontWeight: '600' }}>WiFi Connectivity:</label>
          <button
            onClick={() => setIsOnline(!isOnline)}
            style={{
              padding: '4px 10px',
              borderRadius: '4px',
              border: 'none',
              fontWeight: '700',
              fontSize: '0.75rem',
              background: isOnline ? '#dcfce7' : '#fee2e2',
              color: isOnline ? '#15803d' : '#991b1b'
            }}
          >
            {isOnline ? 'ONLINE (WiFi Connected)' : 'OFFLINE (Dead Zone)'}
          </button>
        </div>
      </div>

      {message && (
        <div style={{ padding: '1rem', borderRadius: '6px', marginBottom: '1.5rem', background: '#e0f2fe', color: '#0369a1', border: '1px solid #bae6fd' }}>
          {message}
        </div>
      )}

      {/* Terminal Controls */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
        <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '1rem' }}>Barcode Ingestion Trigger</h3>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '4px' }}>Device Node ID</label>
            <input type="text" value={nodeId} onChange={(e) => setNodeId(e.target.value)} style={{ width: '100%', padding: '6px', border: '1px solid #cbd5e1', borderRadius: '4px' }} />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '4px' }}>Scanned SKU</label>
            <select value={sku} onChange={(e) => setSku(e.target.value)} style={{ width: '100%', padding: '6px', border: '1px solid #cbd5e1', borderRadius: '4px' }}>
              <option value="SKU-LAPTOP-001">SKU-LAPTOP-001 (High-Performance Laptop)</option>
              <option value="SKU-PHONE-002">SKU-PHONE-002 (5G Smartphone)</option>
              <option value="SKU-HEADSET-003">SKU-HEADSET-003 (Wireless Headphones)</option>
              <option value="SKU-LIMITED-999">SKU-LIMITED-999 (Limited Keyboard)</option>
            </select>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '1.25rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '4px' }}>Quantity Received</label>
              <input type="number" min="1" value={qty} onChange={(e) => setQty(parseInt(e.target.value))} style={{ width: '100%', padding: '6px', border: '1px solid #cbd5e1', borderRadius: '4px' }} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '4px' }}>Warehouse Region</label>
              <select value={region} onChange={(e) => setRegion(e.target.value)} style={{ width: '100%', padding: '6px', border: '1px solid #cbd5e1', borderRadius: '4px' }}>
                <option value="US-EAST">US-EAST</option>
                <option value="EU-CENTRAL">EU-CENTRAL</option>
                <option value="APAC-SOUTH">APAC-SOUTH</option>
                <option value="UK-SOUTH">UK-SOUTH</option>
              </select>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              onClick={handleCaptureScan}
              style={{ flex: 1, padding: '8px', background: '#2563eb', color: '#fff', border: 'none', borderRadius: '4px', fontWeight: '600', fontSize: '0.85rem' }}
            >
              Capture Barcode Scan
            </button>
            <button
              onClick={handleSimulateDuplicate}
              style={{ padding: '8px 12px', background: '#f1f5f9', color: '#475569', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '0.8rem' }}
            >
              Add Duplicate Scan
            </button>
          </div>
        </div>

        {/* Offline Buffer View */}
        <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: '700' }}>Local Flash Buffer Queue</h3>
              <span style={{ fontSize: '0.8rem', fontWeight: '600', color: offlineBuffer.length > 4000 ? '#dc2626' : '#2563eb' }}>
                {offlineBuffer.length} / 5,000 Events
              </span>
            </div>
            <div style={{ maxHeight: '180px', overflowY: 'auto', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '4px', padding: '0.5rem', fontSize: '0.75rem', fontFamily: 'monospace' }}>
              {offlineBuffer.length === 0 ? (
                <div style={{ color: '#94a3b8', textAlign: 'center', padding: '1rem' }}>Queue is empty.</div>
              ) : (
                offlineBuffer.map((ev, idx) => (
                  <div key={idx} style={{ marginBottom: '4px', borderBottom: '1px dashed #cbd5e1', paddingBottom: '2px' }}>
                    [{ev.event_id}] {ev.event_type} {ev.quantity}x {ev.sku} ({ev.region_id})
                  </div>
                ))
              )}
            </div>
          </div>

          <div style={{ borderTop: '1px solid #e2e8f0', paddingTop: '1rem', marginTop: '1rem' }}>
            <button
              disabled={offlineBuffer.length === 0}
              onClick={handleSyncBatch}
              style={{
                width: '100%',
                padding: '10px',
                background: offlineBuffer.length > 0 ? (isOnline ? '#16a34a' : '#94a3b8') : '#cbd5e1',
                color: '#fff',
                border: 'none',
                borderRadius: '6px',
                fontWeight: '700',
                fontSize: '0.9rem'
              }}
            >
              {isOnline ? 'Flush & Synchronize Batch to Server' : 'Disabled (Terminal is Offline)'}
            </button>
          </div>
        </div>
      </div>

      {syncResult && (
        <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '0.5rem' }}>Latest Synchronization Results</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', textAlign: 'center' }}>
            <div style={{ background: '#f8fafc', padding: '10px', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Received</div>
              <div style={{ fontSize: '1.25rem', fontWeight: '700' }}>{syncResult.received_count}</div>
            </div>
            <div style={{ background: '#dcfce7', padding: '10px', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.75rem', color: '#166534' }}>Processed (New)</div>
              <div style={{ fontSize: '1.25rem', fontWeight: '700', color: '#166534' }}>{syncResult.processed_count}</div>
            </div>
            <div style={{ background: '#fef3c7', padding: '10px', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.75rem', color: '#b45309' }}>Duplicates Ignored</div>
              <div style={{ fontSize: '1.25rem', fontWeight: '700', color: '#b45309' }}>{syncResult.duplicate_count}</div>
            </div>
            <div style={{ background: '#f1f5f9', padding: '10px', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.75rem', color: '#475569' }}>Stale Observations</div>
              <div style={{ fontSize: '1.25rem', fontWeight: '700', color: '#475569' }}>{syncResult.stale_count}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
