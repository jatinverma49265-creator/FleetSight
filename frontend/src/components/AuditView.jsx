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
      <div style={{ margin: '40px 28px' }}>
        <div className="glass-panel" style={{
          padding: '48px 32px',
          textAlign: 'center',
          maxWidth: '580px',
          margin: '0 auto',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          background: 'var(--color-surface)',
          borderRadius: 'var(--radius-xl)'
        }}>
          <div style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            background: 'rgba(239, 68, 68, 0.12)',
            color: '#ef4444',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 18px auto',
          }}>
            <Lock size={26} />
          </div>
          <h2 style={{ fontSize: '19px', fontWeight: '800', color: 'var(--color-text-primary)', marginBottom: '8px' }}>
            RBAC Access Denied: 403 Forbidden
          </h2>
          <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', lineHeight: '1.6', margin: '0 0 20px 0' }}>
            The immutable audit log is strictly restricted to <b>Municipal Admins</b> and <b>Traffic Police Law Enforcement</b> officers under the DPDP Act 2023 compliance guidelines.
          </p>
          <div style={{
            background: 'var(--color-surface-subtle)',
            border: '1px solid var(--color-border-default)',
            padding: '12px 16px',
            borderRadius: '8px',
            fontSize: '12px',
            color: 'var(--color-text-muted)',
            lineHeight: 1.5
          }}>
            Active Role: <b style={{ color: '#ef4444' }}>{currentRole.toUpperCase()}</b> · Switch role to <b>City Admin</b> or <b>Traffic Police</b> in the top navbar to inspect audit records.
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ margin: '20px 28px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
      
      {/* Header */}
      <div className="glass-panel" style={{ padding: '20px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              background: 'rgba(56, 189, 248, 0.12)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--color-accent)'
            }}>
              <ShieldCheck size={18} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <h2 style={{ fontSize: '17px', fontWeight: '800', color: 'var(--color-text-primary)', margin: 0 }}>
                  Immutable Compliance & Operational Audit Trail
                </h2>
                <span className="badge-simulated">SIMULATED</span>
              </div>
              <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '2px', margin: 0 }}>
                DPDP Act 2023 Purpose Limitation & Security Audit Log · Access restricted to Admin & Police
              </p>
            </div>
          </div>
        </div>

        <div style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>
          Authorized Session: <b style={{ color: 'var(--color-accent)' }}>{currentRole.toUpperCase()}</b>
        </div>
      </div>

      {/* Table */}
      <div className="glass-panel" style={{ padding: '18px 22px', overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--color-border-default)', textAlign: 'left', color: 'var(--color-text-muted)' }}>
              <th style={{ padding: '12px 10px', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>TIMESTAMP</th>
              <th style={{ padding: '12px 10px', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>ACTION</th>
              <th style={{ padding: '12px 10px', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>USER / ACTOR</th>
              <th style={{ padding: '12px 10px', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>ROLE</th>
              <th style={{ padding: '12px 10px', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>RESOURCE</th>
              <th style={{ padding: '12px 10px', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>DETAILS</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((entry) => (
              <tr key={entry.audit_id} style={{ borderBottom: '1px solid var(--color-border-subtle)', transition: 'background var(--transition-fast)' }}>
                <td style={{ padding: '12px 10px', color: 'var(--color-text-muted)', fontFamily: 'var(--font-mono)' }}>
                  {new Date(entry.timestamp).toLocaleTimeString()}
                </td>
                <td style={{ padding: '12px 10px', fontWeight: '700', color: 'var(--color-accent)' }}>
                  {entry.action}
                </td>
                <td style={{ padding: '12px 10px', color: 'var(--color-text-primary)' }}>
                  {entry.username}
                </td>
                <td style={{ padding: '12px 10px' }}>
                  <span style={{
                    background: 'var(--color-surface-elevated)',
                    border: '1px solid var(--color-border-default)',
                    padding: '3px 7px',
                    borderRadius: '4px',
                    fontSize: '10px',
                    textTransform: 'uppercase',
                    color: 'var(--color-text-secondary)',
                    fontWeight: 600
                  }}>
                    {entry.role}
                  </span>
                </td>
                <td style={{ padding: '12px 10px', fontFamily: 'var(--font-mono)', color: 'var(--color-text-muted)' }}>
                  {entry.resource_type}:{entry.resource_id}
                </td>
                <td style={{ padding: '12px 10px', color: 'var(--color-text-secondary)' }}>
                  {entry.details}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}
