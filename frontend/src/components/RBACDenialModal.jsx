import React from 'react';
import { ShieldAlert, X } from 'lucide-react';

export default function RBACDenialModal({ isOpen, message, onClose, currentRole }) {
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
        id="rbac-denial-modal"
        className="glass-panel"
        style={{
          width: '100%',
          maxWidth: '480px',
          padding: '28px',
          border: '1px solid rgba(239, 68, 68, 0.4)',
          boxShadow: 'var(--shadow-lg)',
          background: 'var(--color-surface)',
          borderRadius: 'var(--radius-xl)'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '10px',
              background: 'rgba(239, 68, 68, 0.12)',
              color: '#ef4444',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <ShieldAlert size={22} />
            </div>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: '800', color: 'var(--color-text-primary)', margin: 0 }}>
                RBAC Access Denied (403)
              </h3>
              <span style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>
                Role-Based Access Control Enforcement
              </span>
            </div>
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

        <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', lineHeight: '1.6', marginBottom: '16px' }}>
          {message}
        </p>

        <div style={{
          background: 'var(--color-surface-subtle)',
          border: '1px solid var(--color-border-default)',
          borderRadius: 'var(--radius-md)',
          padding: '14px',
          fontSize: '12px',
          color: 'var(--color-text-muted)',
          marginBottom: '20px',
          lineHeight: 1.5
        }}>
          Current Active Role: <b style={{ color: '#ef4444' }}>{currentRole.toUpperCase()}</b>.<br />
          To perform engineer approvals or state transitions, select <b>PWD Engineer</b> in the top navigation role switcher.
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button
            id="rbac-modal-close-btn"
            onClick={onClose}
            style={{
              background: 'var(--color-surface-elevated)',
              color: 'var(--color-text-primary)',
              border: '1px solid var(--color-border-default)',
              padding: '8px 20px',
              borderRadius: '8px',
              fontWeight: '700',
              fontSize: '12px',
              cursor: 'pointer',
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
