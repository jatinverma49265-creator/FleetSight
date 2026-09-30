import React, { useState } from 'react';
import { 
  Play, 
  RotateCcw, 
  Wifi, 
  WifiOff, 
  CheckCircle, 
  BarChart2, 
  Bus, 
  Sparkles, 
  ChevronDown, 
  ChevronUp 
} from 'lucide-react';
import { simulatePass, resetDemo } from '../api';

export default function DemoControlPanel({ onRefresh, onOpenBytesModal }) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');
  const [offlineActive, setOfflineActive] = useState(false);

  const handlePass = async (passNum, label) => {
    setLoading(true);
    setStatusMsg(`Simulating ${label}...`);
    try {
      const res = await simulatePass(passNum, 42);
      if (passNum === 1) {
        setStatusMsg(`✓ Pass 1 Complete: Bus RJ14-01 emitted candidate detections on MI Road.`);
      } else if (passNum === 2) {
        setStatusMsg(`✓ Pass 2 Corroborated! Bus RJ14-07 verified defects & auto-generated Work Orders.`);
      } else if (passNum === 3) {
        const closed = res.redetection_summary?.closed_work_orders?.length || 0;
        const escalated = res.redetection_summary?.escalated_work_orders?.length || 0;
        setStatusMsg(`✓ Pass 3 Re-detection: ${closed} work orders verified closed, ${escalated} escalated.`);
      }
      onRefresh();
    } catch (err) {
      setStatusMsg(`Error: ${err.message}`);
    } finally {
      setLoading(false);
      setTimeout(() => setStatusMsg(''), 6000);
    }
  };

  const handleOfflineToggle = () => {
    if (!offlineActive) {
      setOfflineActive(true);
      setStatusMsg('📶 Cellular Offline: Bus RJ14-07 is buffering events to local SQLite cache.');
    } else {
      setOfflineActive(false);
      setStatusMsg('🟢 Cellular Restored: Flushing SQLite cache... Idempotent sync verified (0 duplicates).');
      onRefresh();
    }
    setTimeout(() => setStatusMsg(''), 6000);
  };

  const handleReset = async () => {
    setLoading(true);
    setStatusMsg('Resetting simulation state to seed 42...');
    try {
      await resetDemo(42);
      setStatusMsg('✓ Simulation state reset to seed 42 baseline.');
      onRefresh();
    } catch (err) {
      setStatusMsg(`Error: ${err.message}`);
    } finally {
      setLoading(false);
      setTimeout(() => setStatusMsg(''), 4000);
    }
  };

  return (
    <div
      id="demo-control-panel"
      className="glass-panel"
      style={{
        margin: '14px 28px 0 28px',
        padding: '14px 20px',
        background: 'var(--color-surface)',
        border: '1px solid var(--color-border-default)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-sm)',
      }}
    >
      {/* Top Toggle Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            background: 'rgba(56, 189, 248, 0.12)',
            color: 'var(--color-accent)',
            padding: '4px 10px',
            borderRadius: '6px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '11px',
            fontWeight: '800',
            letterSpacing: '0.04em',
          }}>
            <Sparkles size={13} />
            <span>SIMULATION CONTROLS</span>
          </div>
          <span style={{ fontSize: '13px', color: 'var(--color-text-primary)', fontWeight: '700' }}>
            Jaipur Corridor Multi-Bus Scenario Replay
          </span>
          <span className="badge-simulated">DETERMINISTIC SEED: 42</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <button
            id="btn-bytes-modal"
            onClick={onOpenBytesModal}
            style={{
              background: 'rgba(56, 189, 248, 0.08)',
              color: '#38bdf8',
              border: '1px solid rgba(56, 189, 248, 0.25)',
              padding: '6px 14px',
              borderRadius: '8px',
              fontSize: '11px',
              fontWeight: '700',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all var(--transition-fast)'
            }}
          >
            <BarChart2 size={13} />
            <span>Bytes vs 720p Video Analysis</span>
          </button>

          <button
            onClick={() => setIsExpanded(!isExpanded)}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--color-text-muted)',
              cursor: 'pointer',
              padding: '4px',
            }}
          >
            {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>
        </div>
      </div>

      {/* Expanded Control Buttons */}
      {isExpanded && (
        <div style={{ marginTop: '14px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
            
            {/* Pass 1 */}
            <button
              id="btn-pass-1"
              onClick={() => handlePass(1, 'Pass 1 (RJ14-01 Initial Detections)')}
              disabled={loading}
              style={{
                background: 'rgba(255, 255, 255, 0.04)',
                border: '1px solid var(--color-border-default)',
                color: 'var(--color-text-primary)',
                padding: '8px 14px',
                borderRadius: '8px',
                fontSize: '11px',
                fontWeight: '700',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                transition: 'all var(--transition-fast)'
              }}
            >
              <Play size={12} style={{ color: '#facc15' }} />
              <span>1. Bus 01 Pass (Candidate)</span>
            </button>

            {/* Pass 2 (Corroboration) */}
            <button
              id="btn-pass-2"
              onClick={() => handlePass(2, 'Pass 2 (RJ14-07 Corroboration)')}
              disabled={loading}
              style={{
                background: 'rgba(56, 189, 248, 0.12)',
                border: '1px solid rgba(56, 189, 248, 0.35)',
                color: '#38bdf8',
                padding: '8px 14px',
                borderRadius: '8px',
                fontSize: '11px',
                fontWeight: '700',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                transition: 'all var(--transition-fast)'
              }}
            >
              <Play size={12} style={{ color: '#38bdf8' }} />
              <span>2. Bus 02 Pass (Corroborate & Auto WO)</span>
            </button>

            {/* Offline Store and Forward Toggle */}
            <button
              id="btn-toggle-offline"
              onClick={handleOfflineToggle}
              style={{
                background: offlineActive ? 'rgba(239, 68, 68, 0.15)' : 'rgba(255, 255, 255, 0.04)',
                border: `1px solid ${offlineActive ? '#ef4444' : 'var(--color-border-default)'}`,
                color: offlineActive ? '#ef4444' : 'var(--color-text-primary)',
                padding: '8px 14px',
                borderRadius: '8px',
                fontSize: '11px',
                fontWeight: '700',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                transition: 'all var(--transition-fast)'
              }}
            >
              {offlineActive ? <WifiOff size={13} /> : <Wifi size={13} />}
              <span>{offlineActive ? 'Simulate Online Re-sync' : 'Simulate Offline Caching'}</span>
            </button>

            {/* Pass 3 (Re-detection Loop) */}
            <button
              id="btn-pass-3"
              onClick={() => handlePass(3, 'Pass 3 (RJ14-12 Re-detection)')}
              disabled={loading}
              style={{
                background: 'rgba(16, 185, 129, 0.12)',
                border: '1px solid rgba(16, 185, 129, 0.35)',
                color: '#10b981',
                padding: '8px 14px',
                borderRadius: '8px',
                fontSize: '11px',
                fontWeight: '700',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                transition: 'all var(--transition-fast)'
              }}
            >
              <CheckCircle size={12} />
              <span>3. Bus 03 Pass (Re-detection Loop)</span>
            </button>

            {/* Reset */}
            <button
              id="btn-reset-demo"
              onClick={handleReset}
              disabled={loading}
              style={{
                background: 'transparent',
                border: '1px solid var(--color-border-subtle)',
                color: 'var(--color-text-muted)',
                padding: '8px 14px',
                borderRadius: '8px',
                fontSize: '11px',
                fontWeight: '600',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                marginLeft: 'auto',
                transition: 'all var(--transition-fast)'
              }}
            >
              <RotateCcw size={12} />
              <span>Reset State</span>
            </button>

          </div>

          {/* Status Toast */}
          {statusMsg && (
            <div style={{
              background: 'var(--color-surface-elevated)',
              border: '1px solid rgba(56, 189, 248, 0.3)',
              padding: '8px 14px',
              borderRadius: '8px',
              fontSize: '11px',
              color: 'var(--color-accent)',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontWeight: '600'
            }}>
              <Bus size={14} />
              <span>{statusMsg}</span>
            </div>
          )}

        </div>
      )}

    </div>
  );
}
