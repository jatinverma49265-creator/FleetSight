import React from 'react';
import { ShieldAlert, X } from 'lucide-react';

export default function RBACDenialModal({ isOpen, message, onClose, currentRole }) {
  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(13, 27, 42, 0.65)',
      backdropFilter: 'blur(12px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2000,
      padding: '20px',
    }}>
      <div
        id="rbac-denial-modal"
        className="glass-panel animate-fade-in"
        style={{
          width: '100%',
          maxWidth: '480px',
          padding: '28px',
          border: '1px solid rgba(185, 28, 28, 0.3)',
          boxShadow: 'var(--shadow-lg)',
          background: '#FFFFFF',
          borderRadius: 'var(--radius-xl)'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '42px',
              height: '42px',
              borderRadius: '10px',
              background: 'rgba(185, 28, 28, 0.1)',
              color: '#b91c1c',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <ShieldAlert size={22} />
            </div>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: '800', color: 'var(--c-rich-navy)', margin: 0 }}>
                RBAC Access Denied (403)
              </h3>
              <span style={{ fontSize: '11px', color: 'var(--c-slate-blue)', fontWeight: 600 }}>
                Role-Based Access Control Enforcement
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            aria-label="Close modal"
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
              boxShadow: 'var(--shadow-sm)'
            }}
          >
            <X size={16} />
          </button>
        </div>

        <p style={{ fontSize: '13px', color: 'var(--c-deep-navy)', lineHeight: '1.6', marginBottom: '16px' }}>
          {message}
        </p>

        <div style={{
          background: 'var(--color-surface-subtle)',
          border: '1px solid var(--color-border-default)',
          borderRadius: 'var(--radius-md)',
          padding: '14px',
          fontSize: '12px',
          color: 'var(--c-slate-blue)',
          marginBottom: '20px',
          lineHeight: 1.5
        }}>
          Current Active Role: <b style={{ color: '#b91c1c' }}>{currentRole.toUpperCase()}</b>.<br />
          To perform engineer approvals or state transitions, select <b>PWD Engineer</b> in the sidebar role switcher.
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button
            id="rbac-modal-close-btn"
            onClick={onClose}
            style={{
              background: 'var(--c-deep-navy)',
              color: '#FFFFFF',
              border: 'none',
              padding: '9px 22px',
              borderRadius: '8px',
              fontWeight: '700',
              fontSize: '12px',
              cursor: 'pointer',
              boxShadow: '0 2px 8px rgba(13, 27, 42, 0.2)',
              transition: 'all var(--transition-fast)'
            }}
          >
            Acknowledge
          </button>
        </div>
      </div>
    </div>
  );
}
