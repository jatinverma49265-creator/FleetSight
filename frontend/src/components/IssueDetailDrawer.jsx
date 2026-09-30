import React from 'react';
import { X, ShieldCheck, Bus, Camera, Clock, MapPin } from 'lucide-react';

export default function IssueDetailDrawer({ issue, onClose }) {
  if (!issue) return null;

  const isVerified = issue.status === 'verified' || issue.status === 'work_order';
  const breakdown = issue.severity_breakdown;

  return (
    <aside
      id="issue-detail-drawer"
      className="glass-panel animate-fade-in"
      style={{
        width: '380px',
        maxHeight: 'calc(100vh - 210px)',
        overflowY: 'auto',
        padding: '22px',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
        background: '#FFFFFF',
        border: '1px solid var(--color-border-default)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-lg)',
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '10px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
            <span style={{
              background: isVerified ? 'rgba(21, 128, 61, 0.12)' : 'rgba(180, 83, 9, 0.12)',
              color: isVerified ? '#15803d' : '#b45309',
              border: `1px solid ${isVerified ? 'rgba(21, 128, 61, 0.35)' : 'rgba(180, 83, 9, 0.35)'}`,
              padding: '2px 8px',
              borderRadius: '4px',
              fontSize: '10px',
              fontWeight: '800',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
            }}>
              {issue.status.replace('_', ' ')}
            </span>
            <span className="badge-simulated">SIMULATED</span>
          </div>
          <h3 style={{ fontSize: '18px', fontWeight: '800', color: 'var(--c-rich-navy)', margin: 0 }}>
            {issue.detection_class.replace('_', ' ').toUpperCase()}
          </h3>
          <p style={{ fontSize: '11px', color: 'var(--c-slate-blue)', marginTop: '2px', margin: 0, fontWeight: 500 }}>
            ID: <span style={{ fontFamily: 'var(--font-mono)' }}>{issue.issue_id}</span>
          </p>
        </div>
        <button
          id="close-drawer-btn"
          aria-label="Close Issue Details"
          onClick={onClose}
          style={{
            background: '#FFFFFF',
            border: '1px solid var(--c-soft-steel)',
            color: 'var(--c-deep-navy)',
            padding: '6px',
            borderRadius: '6px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: 'var(--shadow-sm)',
            transition: 'all var(--transition-fast)'
          }}
        >
          <X size={15} />
        </button>
      </div>

      {/* Blurred Privacy Evidence Frame */}
      <div style={{
        borderRadius: 'var(--radius-md)',
        overflow: 'hidden',
        border: '1px solid var(--color-border-default)',
        background: 'var(--color-surface-subtle)',
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
            background: 'linear-gradient(180deg, var(--c-light-bg) 0%, #D5D7D1 100%)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            color: 'var(--c-slate-blue)',
          }}>
            <Camera size={26} />
            <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--c-deep-navy)' }}>Edge Cropped Sensor Frame</span>
          </div>
        )}

        {/* Privacy filter badge */}
        <div style={{
          position: 'absolute',
          top: '8px',
          right: '8px',
          background: 'rgba(13, 27, 42, 0.92)',
          border: '1px solid rgba(21, 128, 61, 0.4)',
          padding: '3px 8px',
          borderRadius: '4px',
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          fontSize: '9px',
          color: '#22c55e',
          fontWeight: '700',
        }}>
          <ShieldCheck size={12} />
          <span>DPDP ACT 2023 · BLURRED</span>
        </div>

        {/* Bounding Box Simulated Tag */}
        <div style={{
          position: 'absolute',
          bottom: '8px',
          left: '8px',
          background: 'var(--color-safety-orange)',
          color: '#FFFFFF',
          fontSize: '10px',
          fontWeight: '800',
          padding: '2px 8px',
          borderRadius: '4px',
          boxShadow: '0 2px 6px rgba(0,0,0,0.2)'
        }}>
          {issue.detection_class} · {issue.severity.toUpperCase()}
        </div>
      </div>

      {/* Priority Score & Explainability Breakdown */}
      <div style={{
        background: 'var(--color-surface-subtle)',
        border: '1px solid var(--color-border-default)',
        borderRadius: 'var(--radius-md)',
        padding: '16px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <div>
            <div style={{ fontSize: '10px', color: 'var(--c-slate-blue)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: '700' }}>
              Explainable Priority Score
            </div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px', marginTop: '2px' }}>
              <span style={{ fontSize: '32px', fontWeight: '800', color: 'var(--c-deep-navy)', fontVariantNumeric: 'tabular-nums' }}>
                {issue.priority_score}
              </span>
              <span style={{ fontSize: '12px', color: 'var(--c-slate-blue)', fontWeight: 600 }}>/ 100</span>
            </div>
          </div>
          <div style={{
            background: 'rgba(27, 38, 59, 0.1)',
            border: '1px solid rgba(27, 38, 59, 0.25)',
            borderRadius: '6px',
            padding: '4px 10px',
            fontSize: '11px',
            color: 'var(--c-deep-navy)',
            fontWeight: '700',
          }}>
            {issue.observation_count >= 2 ? 'Corroborated' : 'Single Pass'}
          </div>
        </div>

        {/* Explainability Breakdown Bars */}
        {breakdown && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '10px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--c-deep-navy)', fontWeight: 600 }}>
                <span>Defect Severity ({breakdown.severity_level})</span>
                <strong style={{ color: '#b91c1c' }}>+{breakdown.severity_weight} / 40</strong>
              </div>
              <div style={{ width: '100%', height: '6px', background: 'rgba(119, 141, 169, 0.25)', borderRadius: '3px', overflow: 'hidden', marginTop: '3px' }}>
                <div style={{ width: `${(breakdown.severity_weight / 40) * 100}%`, height: '100%', background: '#b91c1c' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--c-deep-navy)', fontWeight: 600 }}>
                <span>Multi-Bus Recurrence ({issue.observation_count} passes)</span>
                <strong style={{ color: 'var(--c-deep-navy)' }}>+{breakdown.recurrence_weight} / 30</strong>
              </div>
              <div style={{ width: '100%', height: '6px', background: 'rgba(119, 141, 169, 0.25)', borderRadius: '3px', overflow: 'hidden', marginTop: '3px' }}>
                <div style={{ width: `${(breakdown.recurrence_weight / 30) * 100}%`, height: '100%', background: 'var(--c-deep-navy)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--c-deep-navy)', fontWeight: 600 }}>
                <span>Corridor Context ({breakdown.road_classification})</span>
                <strong style={{ color: 'var(--c-slate-blue)' }}>+{breakdown.context_weight} / 20</strong>
              </div>
              <div style={{ width: '100%', height: '6px', background: 'rgba(119, 141, 169, 0.25)', borderRadius: '3px', overflow: 'hidden', marginTop: '3px' }}>
                <div style={{ width: `${(breakdown.context_weight / 20) * 100}%`, height: '100%', background: 'var(--c-slate-blue)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--c-deep-navy)', fontWeight: 600 }}>
                <span>Detector Confidence</span>
                <strong style={{ color: '#b45309' }}>+{breakdown.confidence_weight} / 10</strong>
              </div>
              <div style={{ width: '100%', height: '6px', background: 'rgba(119, 141, 169, 0.25)', borderRadius: '3px', overflow: 'hidden', marginTop: '3px' }}>
                <div style={{ width: `${(breakdown.confidence_weight / 10) * 100}%`, height: '100%', background: '#b45309' }} />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Observation Metadata List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--c-slate-blue)' }}>
          <MapPin size={14} style={{ color: 'var(--c-deep-navy)' }} />
          <span>{issue.road_segment}</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--c-slate-blue)' }}>
          <Bus size={14} style={{ color: 'var(--c-deep-navy)' }} />
          <span>
            Buses: <strong style={{ color: 'var(--c-rich-navy)' }}>{issue.bus_ids.join(', ') || 'N/A'}</strong> ({issue.observation_count} total passes)
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--c-slate-blue)' }}>
          <Camera size={14} style={{ color: 'var(--c-slate-blue)' }} />
          <span>Cameras: {issue.camera_ids.join(', ') || 'N/A'}</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--c-slate-blue)' }}>
          <Clock size={14} style={{ color: '#b45309' }} />
          <span>Last detected: {new Date(issue.last_detected_at).toLocaleTimeString()}</span>
        </div>
      </div>

    </aside>
  );
}
