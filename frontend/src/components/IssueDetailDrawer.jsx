import React from 'react';
import { X, CheckCircle2, AlertTriangle, ShieldCheck, Bus, Camera, Clock, MapPin, Sparkles } from 'lucide-react';

export default function IssueDetailDrawer({ issue, onClose, onPromoteToWorkOrder }) {
  if (!issue) return null;

  const isVerified = issue.status === 'verified' || issue.status === 'work_order';
  const breakdown = issue.severity_breakdown;

  return (
    <aside
      id="issue-detail-drawer"
      className="glass-panel"
      style={{
        width: '380px',
        maxHeight: 'calc(100vh - 200px)',
        overflowY: 'auto',
        padding: '20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
        border: '1px solid var(--border-subtle)',
        boxShadow: '0 12px 40px rgba(0,0,0,0.6)',
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '10px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
            <span style={{
              background: isVerified ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
              color: isVerified ? '#10b981' : '#f59e0b',
              border: `1px solid ${isVerified ? 'rgba(16, 185, 129, 0.4)' : 'rgba(245, 158, 11, 0.4)'}`,
              padding: '2px 8px',
              borderRadius: '4px',
              fontSize: '10px',
              fontWeight: '800',
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
            }}>
              {issue.status.replace('_', ' ')}
            </span>
            <span className="badge-simulated">SIMULATED</span>
          </div>
          <h3 style={{ fontSize: '18px', fontWeight: '800', color: '#fff' }}>
            {issue.detection_class.replace('_', ' ').toUpperCase()}
          </h3>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>
            ID: <span style={{ fontFamily: 'var(--font-mono)' }}>{issue.issue_id}</span>
          </p>
        </div>
        <button
          id="close-drawer-btn"
          onClick={onClose}
          style={{
            background: 'rgba(255,255,255,0.05)',
            border: 'none',
            color: 'var(--text-muted)',
            padding: '6px',
            borderRadius: '6px',
            cursor: 'pointer',
          }}
        >
          <X size={16} />
        </button>
      </div>

      {/* Blurred Privacy Evidence Frame */}
      <div style={{
        borderRadius: '8px',
        overflow: 'hidden',
        border: '1px solid var(--border-subtle)',
        background: '#09131c',
        position: 'relative',
      }}>
        {issue.evidence_uri ? (
          <img
            src={issue.evidence_uri}
            alt="Evidence"
            style={{ width: '100%', height: '180px', objectFit: 'cover', filter: 'blur(0.5px)' }}
          />
        ) : (
          <div style={{
            height: '160px',
            background: 'linear-gradient(180deg, #182836 0%, #0d1720 100%)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            color: 'var(--text-dim)',
          }}>
            <Camera size={28} />
            <span style={{ fontSize: '11px' }}>Edge Cropped Frame</span>
          </div>
        )}

        {/* Privacy filter badge */}
        <div style={{
          position: 'absolute',
          top: '8px',
          right: '8px',
          background: 'rgba(7, 13, 19, 0.9)',
          border: '1px solid rgba(0, 210, 180, 0.3)',
          padding: '3px 8px',
          borderRadius: '4px',
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          fontSize: '9px',
          color: '#00d2b4',
          fontWeight: '700',
        }}>
          <ShieldCheck size={12} />
          <span>FACES & PLATES BLURRED</span>
        </div>

        {/* Bounding Box Simulated Tag */}
        <div style={{
          position: 'absolute',
          bottom: '8px',
          left: '8px',
          background: 'rgba(255, 122, 0, 0.9)',
          color: '#fff',
          fontSize: '10px',
          fontWeight: '800',
          padding: '2px 6px',
          borderRadius: '3px',
        }}>
          {issue.detection_class} · {issue.severity.toUpperCase()}
        </div>
      </div>

      {/* Priority Score & Explainability Breakdown */}
      <div style={{
        background: 'rgba(255,255,255,0.02)',
        border: '1px solid var(--border-subtle)',
        borderRadius: '8px',
        padding: '14px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
          <div>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: '700' }}>
              Explainable Priority Score
            </div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
              <span style={{ fontSize: '32px', fontWeight: '800', color: 'var(--brand-teal)' }}>
                {issue.priority_score}
              </span>
              <span style={{ fontSize: '12px', color: 'var(--text-dim)' }}>/ 100</span>
            </div>
          </div>
          <div style={{
            background: 'rgba(0, 210, 180, 0.1)',
            border: '1px solid rgba(0, 210, 180, 0.3)',
            borderRadius: '6px',
            padding: '4px 8px',
            fontSize: '11px',
            color: 'var(--brand-teal)',
            fontWeight: '700',
          }}>
            {issue.observation_count >= 2 ? 'Corroborated' : 'Single Pass'}
          </div>
        </div>

        {/* Explainability Breakdown Bars */}
        {breakdown && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '10px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
                <span>Defect Severity ({breakdown.severity_level})</span>
                <b style={{ color: '#fff' }}>+{breakdown.severity_weight} / 40</b>
              </div>
              <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.08)', borderRadius: '2px', overflow: 'hidden', marginTop: '2px' }}>
                <div style={{ width: `${(breakdown.severity_weight / 40) * 100}%`, height: '100%', background: '#ef4444' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
                <span>Multi-Bus Recurrence ({issue.observation_count} passes)</span>
                <b style={{ color: '#fff' }}>+{breakdown.recurrence_weight} / 30</b>
              </div>
              <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.08)', borderRadius: '2px', overflow: 'hidden', marginTop: '2px' }}>
                <div style={{ width: `${(breakdown.recurrence_weight / 30) * 100}%`, height: '100%', background: '#00d2b4' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
                <span>Corridor Context ({breakdown.road_classification})</span>
                <b style={{ color: '#fff' }}>+{breakdown.context_weight} / 20</b>
              </div>
              <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.08)', borderRadius: '2px', overflow: 'hidden', marginTop: '2px' }}>
                <div style={{ width: `${(breakdown.context_weight / 20) * 100}%`, height: '100%', background: '#3b82f6' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
                <span>Detector Confidence</span>
                <b style={{ color: '#fff' }}>+{breakdown.confidence_weight} / 10</b>
              </div>
              <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.08)', borderRadius: '2px', overflow: 'hidden', marginTop: '2px' }}>
                <div style={{ width: `${(breakdown.confidence_weight / 10) * 100}%`, height: '100%', background: '#eab308' }} />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Observation Metadata List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '11px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)' }}>
          <MapPin size={14} style={{ color: 'var(--brand-teal)' }} />
          <span>{issue.road_segment}</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)' }}>
          <Bus size={14} style={{ color: '#3b82f6' }} />
          <span>
            Buses: <b>{issue.bus_ids.join(', ') || 'N/A'}</b> ({issue.observation_count} total passes)
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)' }}>
          <Camera size={14} style={{ color: '#a855f7' }} />
          <span>Cameras: {issue.camera_ids.join(', ') || 'N/A'}</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)' }}>
          <Clock size={14} style={{ color: '#eab308' }} />
          <span>Last detected: {new Date(issue.last_detected_at).toLocaleTimeString()}</span>
        </div>
      </div>

    </aside>
  );
}
