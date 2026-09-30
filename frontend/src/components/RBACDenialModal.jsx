import React from 'react';
import { ShieldAlert, X, Lock } from 'lucide-react';

export default function RBACDenialModal({ isOpen, message, onClose, currentRole }) {
  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(0, 0, 0, 0.75)',
      backdropFilter: 'blur(8px)',
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
          border: '1px solid rgba(239, 68, 68, 0.5)',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.8)',
          background: 'rgba(15, 23, 33, 0.98)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '8px',
              background: 'rgba(239, 68, 68, 0.15)',
              color: '#ef4444',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <ShieldAlert size={22} />
            </div>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: '800', color: '#fff' }}>
                RBAC Access Denied (403)
              </h3>
              <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>
                Role-Based Access Control Enforcement
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
          >
            <X size={18} />
          </button>
        </div>

        <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: '1.6', marginBottom: '16px' }}>
          {message}
        </p>

        <div style={{
          background: 'rgba(0, 0, 0, 0.3)',
          border: '1px solid var(--border-subtle)',
          borderRadius: '8px',
          padding: '12px',
          fontSize: '11px',
          color: 'var(--text-dim)',
          marginBottom: '20px',
        }}>
          Current Active Role: <b style={{ color: '#ef4444' }}>{currentRole.toUpperCase()}</b>.
          To perform engineer approvals or state transitions, select <b>PWD Engineer</b> in the top navigation role switcher.
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button
            id="rbac-modal-close-btn"
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
            Acknowledge
          </button>
        </div>
      </div>
    </div>
  );
}
