import React, { useEffect, useState } from 'react';
import { ShieldCheck, Lock } from 'lucide-react';
import { fetchAuditLogs } from '../api';

export default function AuditView({ currentRole }) {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    let isMounted = true;
    setError('');

    fetchAuditLogs(currentRole, 100)
      .then((data) => {
        if (isMounted) {
          setLogs(data);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err.detail || err.message);
        }
      });

    return () => { isMounted = false; };
  }, [currentRole]);

  // If role is denied (Engineer or Viewer)
  if (error || currentRole === 'engineer' || currentRole === 'viewer') {
    return (
      <div className="animate-fade-in" style={{ margin: '40px 28px' }}>
        <div className="glass-panel" style={{
          padding: '48px 32px',
          textAlign: 'center',
          maxWidth: '580px',
          margin: '0 auto',
          border: '1px solid rgba(185, 28, 28, 0.3)',
          background: '#FFFFFF',
          borderRadius: 'var(--radius-xl)',
          boxShadow: 'var(--shadow-md)'
        }}>
          <div style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            background: 'rgba(185, 28, 28, 0.1)',
            color: '#b91c1c',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 18px auto',
          }}>
            <Lock size={26} />
          </div>
          <h2 style={{ fontSize: '19px', fontWeight: '800', color: 'var(--c-rich-navy)', marginBottom: '8px' }}>
            RBAC Access Denied: 403 Forbidden
          </h2>
          <p style={{ fontSize: '13px', color: 'var(--c-slate-blue)', lineHeight: '1.6', margin: '0 0 20px 0' }}>
            The immutable audit log is strictly restricted to <b>Municipal Admins</b> and <b>Traffic Police Law Enforcement</b> officers under the DPDP Act 2023 compliance guidelines.
          </p>
          <div style={{
            background: 'var(--color-surface-subtle)',
            border: '1px solid var(--color-border-default)',
            padding: '12px 16px',
            borderRadius: '8px',
            fontSize: '12px',
            color: 'var(--c-slate-blue)',
            lineHeight: 1.5
          }}>
            Active Role: <b style={{ color: '#b91c1c' }}>{currentRole.toUpperCase()}</b> · Switch role to <b>City Admin</b> or <b>Traffic Police</b> in the sidebar to inspect audit records.
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="animate-fade-in" style={{ margin: '20px 28px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
      
      {/* Header */}
      <div className="glass-panel" style={{ padding: '20px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              background: 'var(--color-surface-subtle)',
              border: '1px solid var(--color-border-subtle)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--c-deep-navy)'
            }}>
              <ShieldCheck size={18} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <h2 style={{ fontSize: '17px', fontWeight: '800', color: 'var(--c-rich-navy)', margin: 0 }}>
                  Immutable Compliance & Operational Audit Trail
                </h2>
                <span className="badge-simulated">SIMULATED</span>
              </div>
              <p style={{ fontSize: '12px', color: 'var(--c-slate-blue)', marginTop: '2px', margin: 0, fontWeight: 500 }}>
                DPDP Act 2023 § 8(4) compliant append-only ledger · Authorized for <b>{currentRole.toUpperCase()}</b>
              </p>
            </div>
          </div>
        </div>

        <div style={{
          background: 'var(--color-surface-subtle)',
          border: '1px solid var(--color-border-default)',
          padding: '8px 16px',
          borderRadius: 'var(--radius-md)',
          textAlign: 'right',
          boxShadow: 'var(--shadow-sm)'
        }}>
          <div style={{ fontSize: '16px', fontWeight: '800', color: 'var(--c-deep-navy)' }}>
            {logs.length} Events
          </div>
          <div style={{ fontSize: '10px', color: 'var(--c-slate-blue)', textTransform: 'uppercase', fontWeight: 800 }}>
            Appended to Ledger
          </div>
        </div>
      </div>

      {/* Log Feed */}
      <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: 'calc(100vh - 270px)', overflowY: 'auto' }}>
        {logs.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: 'var(--c-slate-blue)' }}>
            No audit records captured yet. Events and state transitions will be logged automatically.
          </div>
        ) : (
          logs.map((log) => (
            <div
              key={log.log_id}
              className="glass-panel-hover"
              style={{
                padding: '12px 16px',
                borderRadius: '8px',
                background: '#FFFFFF',
                border: '1px solid var(--color-border-default)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                gap: '16px',
                boxShadow: 'var(--shadow-sm)'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                <span style={{
                  background: 'rgba(27, 38, 59, 0.08)',
                  color: 'var(--c-deep-navy)',
                  border: '1px solid rgba(27, 38, 59, 0.2)',
                  padding: '3px 8px',
                  borderRadius: '4px',
                  fontSize: '10px',
                  fontWeight: '800',
                  textTransform: 'uppercase',
                  letterSpacing: '0.04em'
                }}>
                  {log.action}
                </span>

                <div>
                  <div style={{ fontSize: '13px', fontWeight: '700', color: 'var(--c-rich-navy)' }}>
                    {log.description}
                  </div>
                  <div style={{ fontSize: '11px', color: 'var(--c-slate-blue)', marginTop: '2px' }}>
                    Actor: <b style={{ color: 'var(--c-deep-navy)' }}>{log.actor_user_id}</b> ({log.actor_role}) · Target: {log.target_type} ({log.target_id || 'Global'})
                  </div>
                </div>
              </div>

              <div style={{ textAlign: 'right' }}>
                <span style={{ fontSize: '11px', color: 'var(--c-slate-blue)', fontVariantNumeric: 'tabular-nums', fontWeight: 600 }}>
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
                <div style={{ fontSize: '9px', color: 'var(--c-soft-steel)', textTransform: 'uppercase' }}>
                  {new Date(log.timestamp).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

    </div>
  );
}
