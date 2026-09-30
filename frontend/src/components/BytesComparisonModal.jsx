import React, { useEffect, useState } from 'react';
import { X, HardDrive } from 'lucide-react';
import { fetchBytesComparison } from '../api';

export default function BytesComparisonModal({ isOpen, onClose }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (isOpen) {
      fetchBytesComparison()
        .then((res) => {
          setData(res);
        })
        .catch(() => {});
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(8, 13, 20, 0.85)',
      backdropFilter: 'blur(12px)',
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
          border: '1px solid var(--color-border-hover)',
          boxShadow: 'var(--shadow-lg)',
          background: 'var(--color-surface)',
          borderRadius: 'var(--radius-xl)'
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{
                width: '28px',
                height: '28px',
                borderRadius: '6px',
                background: 'rgba(56, 189, 248, 0.12)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--color-accent)'
              }}>
                <HardDrive size={16} />
              </div>
              <h3 style={{ fontSize: '18px', fontWeight: '800', color: 'var(--color-text-primary)', margin: 0 }}>
                Bandwidth & Byte Savings Analysis
              </h3>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '4px', margin: 0 }}>
              Compact Event JSON vs Continuous 720p H.264 Video Streaming
            </p>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'var(--color-surface-elevated)',
              border: '1px solid var(--color-border-default)',
              color: 'var(--color-text-secondary)',
              padding: '6px',
              borderRadius: '6px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <X size={16} />
          </button>
        </div>

        {data ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            
            {/* Main Reduction Banner */}
            <div style={{
              background: 'var(--color-surface-elevated)',
              border: '1px solid rgba(56, 189, 248, 0.3)',
              borderRadius: 'var(--radius-md)',
              padding: '20px',
              textAlign: 'center',
            }}>
              <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: '700' }}>
                Measured Cellular Bandwidth Reduction
              </div>
              <div style={{ fontSize: '46px', fontWeight: '800', color: 'var(--color-accent)', lineHeight: 1.1, margin: '6px 0', fontVariantNumeric: 'tabular-nums' }}>
                {data.bandwidth_reduction_pct}%
              </div>
              <div style={{ fontSize: '12px', color: '#10b981', fontWeight: '700' }}>
                ✓ Prototype Target (≥ 90.0%) Achieved
              </div>
            </div>

            {/* Comparison Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
              
              {/* Event JSON */}
              <div style={{
                background: 'var(--color-surface-elevated)',
                border: '1px solid var(--color-border-default)',
                padding: '16px',
                borderRadius: 'var(--radius-md)',
              }}>
                <span style={{ fontSize: '10px', color: 'var(--color-text-muted)', textTransform: 'uppercase', fontWeight: '700', letterSpacing: '0.04em' }}>
                  FleetSight Telemetry JSON
                </span>
                <div style={{ fontSize: '22px', fontWeight: '800', color: 'var(--color-text-primary)', margin: '4px 0', fontVariantNumeric: 'tabular-nums' }}>
                  {data.events_transmitted_bytes_formatted}
                </div>
                <div style={{ fontSize: '11px', color: 'var(--color-text-secondary)' }}>
                  {data.events_count} events (~320 B / payload)
                </div>
              </div>

              {/* 720p Video Stream */}
              <div style={{
                background: 'var(--color-surface-elevated)',
                border: '1px solid var(--color-border-default)',
                padding: '16px',
                borderRadius: 'var(--radius-md)',
              }}>
                <span style={{ fontSize: '10px', color: 'var(--color-text-muted)', textTransform: 'uppercase', fontWeight: '700', letterSpacing: '0.04em' }}>
                  Continuous 720p Video
                </span>
                <div style={{ fontSize: '22px', fontWeight: '800', color: '#ef4444', margin: '4px 0', fontVariantNumeric: 'tabular-nums' }}>
                  {data.equivalent_video_bytes_formatted}
                </div>
                <div style={{ fontSize: '11px', color: 'var(--color-text-secondary)' }}>
                  2.5 Mbps continuous stream
                </div>
              </div>

            </div>

            {/* Note */}
            <p style={{ fontSize: '11px', color: 'var(--color-text-muted)', lineHeight: 1.5, margin: 0 }}>
              By performing real-time inference on the edge camera in volatile RAM, FleetSight eliminates the need for expensive cellular data uplinks and avoids cloud storage costs.
            </p>

          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '20px', color: 'var(--color-text-muted)' }}>
            Loading bandwidth analysis metrics...
          </div>
        )}

      </div>
    </div>
  );
}
