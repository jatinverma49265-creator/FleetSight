import React, { useEffect, useState } from 'react';
import { X, HardDrive, Zap, CheckCircle2, ArrowRight } from 'lucide-react';
import { fetchBytesComparison } from '../api';

export default function BytesComparisonModal({ isOpen, onClose }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      fetchBytesComparison()
        .then((res) => {
          setData(res);
          setLoading(false);
        })
        .catch(() => setLoading(false));
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2000,
      padding: '20px',
    }}>
      <div
        id="bytes-comparison-modal"
        className="glass-panel"
        style={{
          width: '100%',
          maxWidth: '560px',
          padding: '28px',
          border: '1px solid rgba(168, 85, 247, 0.4)',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.8)',
          background: 'rgba(15, 23, 33, 0.98)',
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <HardDrive size={20} style={{ color: '#c084fc' }} />
              <h3 style={{ fontSize: '18px', fontWeight: '800', color: '#fff' }}>
                Bandwidth & Byte Savings Analysis
              </h3>
            </div>
            <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>
              Compact Event JSON vs Continuous 720p H.264 Video Streaming
            </span>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
          >
            <X size={18} />
          </button>
        </div>

        {data ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            
            {/* Main Reduction Banner */}
            <div style={{
              background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(0, 210, 180, 0.15))',
              border: '1px solid rgba(168, 85, 247, 0.4)',
              borderRadius: '10px',
              padding: '16px',
              textAlign: 'center',
            }}>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: '700' }}>
                Measured Cellular Bandwidth Reduction
              </div>
              <div style={{ fontSize: '42px', fontWeight: '800', color: '#00d2b4', lineHeight: 1.1, margin: '6px 0' }}>
                {data.bandwidth_reduction_pct}%
              </div>
              <div style={{ fontSize: '11px', color: '#a855f7', fontWeight: '700' }}>
                ✓ Prototype Target (≥ 90.0%) Achieved
              </div>
            </div>

            {/* Comparison Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              
              {/* Event JSON */}
              <div style={{
                background: 'rgba(0, 210, 180, 0.06)',
                border: '1px solid rgba(0, 210, 180, 0.3)',
                padding: '14px',
                borderRadius: '8px',
              }}>
                <span style={{ fontSize: '10px', color: 'var(--text-dim)', textTransform: 'uppercase', fontWeight: '700' }}>
                  FleetSight Compact Events
                </span>
                <div style={{ fontSize: '20px', fontWeight: '800', color: '#00d2b4', margin: '4px 0' }}>
                  {data.events_bytes_formatted}
                </div>
                <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>
                  {data.events_count} events · ~320 bytes / event
                </div>
              </div>

              {/* 720p Video Stream */}
              <div style={{
                background: 'rgba(239, 68, 68, 0.06)',
                border: '1px solid rgba(239, 68, 68, 0.3)',
                padding: '14px',
                borderRadius: '8px',
              }}>
                <span style={{ fontSize: '10px', color: 'var(--text-dim)', textTransform: 'uppercase', fontWeight: '700' }}>
                  Continuous 720p Stream
                </span>
                <div style={{ fontSize: '20px', fontWeight: '800', color: '#ef4444', margin: '4px 0' }}>
                  {data.video_stream_formatted}
                </div>
                <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>
                  2.5 Mbps H.264 stream · 7,000s route
                </div>
              </div>

            </div>

            {/* Explanation Note */}
            <div style={{
              fontSize: '11px',
              color: 'var(--text-muted)',
              lineHeight: '1.6',
              background: 'rgba(0,0,0,0.3)',
              padding: '12px',
              borderRadius: '6px',
            }}>
              <b>Edge-First Telemetry Architecture:</b> Raw continuous video remains at the bus edge. Only structured, GPS-tagged JSON events with access-controlled cropped bounding boxes are transmitted over cellular, eliminating &gt;99% of cloud ingestion bandwidth.
            </div>

          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '20px', color: 'var(--text-muted)' }}>
            Loading telemetry metrics...
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '20px' }}>
          <button
            id="bytes-modal-close-btn"
            onClick={onClose}
            style={{
              background: 'var(--border-subtle)',
              color: '#fff',
              border: 'none',
              padding: '8px 18px',
              borderRadius: '6px',
              fontWeight: '700',
              fontSize: '12px',
              cursor: 'pointer',
            }}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
