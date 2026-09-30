import React, { useEffect, useState } from 'react';
import { ShieldCheck, ShieldAlert, Lock, UserCheck, Clock, FileText } from 'lucide-react';
import { fetchAuditLogs } from '../api';

export default function AuditView({ currentRole }) {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    setError('');

    fetchAuditLogs(currentRole, 100)
      .then((data) => {
        if (isMounted) {
          setLogs(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err.detail || err.message);
          setLoading(false);
        }
      });

    return () => { isMounted = false; };
  }, [currentRole]);

  // If role is denied (Engineer or Viewer)
  if (error || currentRole === 'engineer' || currentRole === 'viewer') {
    return (
      <div style={{ margin: '30px 24px' }}>
        <div className="glass-panel" style={{
          padding: '40px',
          textAlign: 'center',
          maxWidth: '600px',
          margin: '0 auto',
          border: '1px solid rgba(239, 68, 68, 0.4)',
          background: 'rgba(239, 68, 68, 0.05)',
        }}>
          <div style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            background: 'rgba(239, 68, 68, 0.15)',
            color: '#ef4444',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 16px auto',
          }}>
            <Lock size={28} />
          </div>
          <h2 style={{ fontSize: '20px', fontWeight: '800', color: '#fff', marginBottom: '8px' }}>
            RBAC Access Denied: 403 Forbidden
          </h2>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: '1.6' }}>
            The immutable audit log is strictly restricted to <b>Municipal Admins</b> and <b>Traffic Police Law Enforcement</b> officers under the DPDP Act 2023 compliance guidelines.
          </p>
          <div style={{
            marginTop: '20px',
            background: 'rgba(0,0,0,0.4)',
            padding: '12px',
            borderRadius: '6px',
            fontSize: '11px',
            color: 'var(--text-dim)',
          }}>
            Active Role: <b style={{ color: '#ef4444' }}>{currentRole.toUpperCase()}</b> · Switch role to <b>City Admin</b> or <b>Traffic Police</b> in the top navbar to inspect audit records.
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ margin: '20px 24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
      
      {/* Header */}
      <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldCheck size={20} style={{ color: 'var(--brand-teal)' }} />
            <h2 style={{ fontSize: '18px', fontWeight: '800', color: '#fff' }}>
              Immutable Compliance & Operational Audit Trail
            </h2>
            <span className="badge-simulated">SIMULATED</span>
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
            DPDP Act 2023 Purpose Limitation & Security Audit Log · Access restricted to Admin & Police
          </p>
        </div>

        <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
          Authorized Session: <b style={{ color: '#00d2b4' }}>{currentRole.toUpperCase()}</b>
        </div>
      </div>

      {/* Table */}
      <div className="glass-panel" style={{ padding: '16px', overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '11px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-subtle)', textAlign: 'left', color: 'var(--text-dim)' }}>
              <th style={{ padding: '10px' }}>TIMESTAMP</th>
              <th style={{ padding: '10px' }}>ACTION</th>
              <th style={{ padding: '10px' }}>USER / ACTOR</th>
              <th style={{ padding: '10px' }}>ROLE</th>
              <th style={{ padding: '10px' }}>RESOURCE</th>
              <th style={{ padding: '10px' }}>DETAILS</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((entry) => (
              <tr key={entry.audit_id} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                <td style={{ padding: '10px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                  {new Date(entry.timestamp).toLocaleTimeString()}
                </td>
                <td style={{ padding: '10px', fontWeight: '700', color: '#00d2b4' }}>
                  {entry.action}
                </td>
                <td style={{ padding: '10px', color: '#fff' }}>
                  {entry.username}
                </td>
                <td style={{ padding: '10px' }}>
                  <span style={{
                    background: 'rgba(255,255,255,0.06)',
                    padding: '2px 6px',
                    borderRadius: '4px',
                    fontSize: '10px',
                    textTransform: 'uppercase',
                    color: '#889ba8',
                  }}>
                    {entry.role}
                  </span>
                </td>
                <td style={{ padding: '10px', fontFamily: 'var(--font-mono)', color: 'var(--text-dim)' }}>
                  {entry.resource_type}:{entry.resource_id}
                </td>
                <td style={{ padding: '10px', color: 'var(--text-muted)' }}>
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
