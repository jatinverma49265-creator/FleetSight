import React, { useState } from 'react';
import { 
  CheckCircle2, 
  UserCheck, 
  Check, 
} from 'lucide-react';
import { updateWorkOrder } from '../api';

export default function WorkOrdersView({ workOrders, currentRole, onRefresh, onTriggerDenialModal }) {
  const [selectedWO, setSelectedWO] = useState(workOrders[0] || null);
  const [actionLoading, setActionLoading] = useState(false);
  const [actionSuccess, setActionSuccess] = useState('');

  const handleAction = async (status, assignedTo = null) => {
    // If role is viewer or police, trigger denial modal to illustrate RBAC enforcement
    if (currentRole === 'viewer' || currentRole === 'police') {
      onTriggerDenialModal(`Role '${currentRole}' is not permitted to modify maintenance work orders. Only PWD Engineers and Municipal Admins hold workflow approval authority.`);
      return;
    }

    if (!selectedWO) return;
    setActionLoading(true);
    setActionSuccess('');

    try {
      const updated = await updateWorkOrder(
        selectedWO.work_order_id,
        {
          status,
          assigned_to: assignedTo || selectedWO.assigned_to || 'PWD Jaipur Division 1 Road Crew',
          comment: `Work order updated to ${status} by ${currentRole}.`,
        },
        currentRole
      );
      setSelectedWO(updated);
      setActionSuccess(`Successfully transitioned to ${status.toUpperCase()}!`);
      setTimeout(() => setActionSuccess(''), 4000);
      onRefresh();
    } catch (err) {
      onTriggerDenialModal(err.detail || err.message);
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '1.2fr 1.8fr',
      gap: '20px',
      margin: '20px 28px',
      minHeight: 'calc(100vh - 220px)',
    }}>
      
      {/* Left Column: Ranked Work Orders List */}
      <div className="glass-panel" style={{ padding: '22px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h2 style={{ fontSize: '17px', fontWeight: '800', color: 'var(--color-text-primary)', margin: 0 }}>
              Ranked Work-Order Queue
            </h2>
            <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '2px', margin: 0 }}>
              Prioritised candidates generated via 2+ bus corroboration
            </p>
          </div>
          <span className="badge-simulated">SIMULATED</span>
        </div>

        {/* Work Order Cards */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflowY: 'auto', maxHeight: 'calc(100vh - 300px)' }}>
          {workOrders.map((wo) => {
            const isSelected = selectedWO?.work_order_id === wo.work_order_id;
            let statusColor = '#facc15';
            if (wo.status === 'assigned' || wo.status === 'in_progress') statusColor = '#38bdf8';
            else if (wo.status === 'completed' || wo.status === 'closed') statusColor = '#10b981';

            return (
              <div
                key={wo.work_order_id}
                id={`wo-card-${wo.work_order_id}`}
                onClick={() => setSelectedWO(wo)}
                className="glass-panel-hover"
                style={{
                  padding: '14px 16px',
                  borderRadius: 'var(--radius-md)',
                  background: isSelected ? 'rgba(56, 189, 248, 0.1)' : 'var(--color-surface-elevated)',
                  border: isSelected ? '1px solid var(--color-accent)' : '1px solid var(--color-border-default)',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '12px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: '8px',
                    background: 'var(--color-surface-subtle)',
                    border: '1px solid var(--color-border-default)',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}>
                    <span style={{ fontSize: '15px', fontWeight: '800', color: 'var(--color-accent)', fontVariantNumeric: 'tabular-nums' }}>
                      {wo.priority_score}
                    </span>
                    <span style={{ fontSize: '7px', color: 'var(--color-text-muted)', textTransform: 'uppercase', fontWeight: 700 }}>
                      SCORE
                    </span>
                  </div>

                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <strong style={{ fontSize: '13px', color: 'var(--color-text-primary)' }}>{wo.title}</strong>
                    </div>
                    <div style={{ fontSize: '11px', color: 'var(--color-text-secondary)', marginTop: '2px' }}>
                      {wo.road_segment} · <b style={{ color: 'var(--color-text-primary)' }}>{wo.observation_count} bus passes</b>
                    </div>
                  </div>
                </div>

                <div style={{ textAlign: 'right' }}>
                  <span style={{
                    background: `${statusColor}18`,
                    color: statusColor,
                    border: `1px solid ${statusColor}40`,
                    padding: '3px 8px',
                    borderRadius: '4px',
                    fontSize: '10px',
                    fontWeight: '700',
                    textTransform: 'uppercase',
                    letterSpacing: '0.04em'
                  }}>
                    {wo.status}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Right Column: Work Order Detail & Engineer Action Panel */}
      {selectedWO ? (
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px', overflowY: 'auto' }}>
          
          {/* Header */}
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--color-accent)', fontWeight: '700' }}>
                  {selectedWO.work_order_id}
                </span>
                <span style={{
                  background: 'rgba(16, 185, 129, 0.12)',
                  color: '#10b981',
                  border: '1px solid rgba(16, 185, 129, 0.35)',
                  padding: '2px 8px',
                  borderRadius: '4px',
                  fontSize: '10px',
                  fontWeight: '700',
                }}>
                  CORROBORATED BY {selectedWO.corroborating_buses.length || 2} BUSES
                </span>
              </div>
              <h1 style={{ fontSize: '20px', fontWeight: '800', color: 'var(--color-text-primary)', margin: '4px 0 0 0' }}>
                {selectedWO.title}
              </h1>
              <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '4px', margin: 0 }}>
                {selectedWO.description}
              </p>
            </div>

            <div style={{
              background: 'var(--color-surface-elevated)',
              border: '1px solid var(--color-border-default)',
              padding: '10px 18px',
              borderRadius: 'var(--radius-md)',
              textAlign: 'center',
              boxShadow: 'var(--shadow-sm)'
            }}>
              <div style={{ fontSize: '26px', fontWeight: '800', color: 'var(--color-accent)', fontVariantNumeric: 'tabular-nums' }}>
                {selectedWO.priority_score}
              </div>
              <div style={{ fontSize: '9px', color: 'var(--color-text-muted)', textTransform: 'uppercase', fontWeight: '700', letterSpacing: '0.04em' }}>
                Priority Score
              </div>
            </div>
          </div>

          {actionSuccess && (
            <div style={{
              background: 'rgba(16, 185, 129, 0.12)',
              border: '1px solid #10b981',
              color: '#10b981',
              padding: '10px 16px',
              borderRadius: '8px',
              fontSize: '12px',
              fontWeight: '700',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}>
              <CheckCircle2 size={16} />
              <span>{actionSuccess}</span>
            </div>
          )}

          {/* Explainability Breakdown Card */}
          <div style={{
            background: 'var(--color-surface-elevated)',
            border: '1px solid var(--color-border-default)',
            borderRadius: 'var(--radius-md)',
            padding: '18px',
          }}>
            <h3 style={{ fontSize: '12px', fontWeight: '700', color: 'var(--color-text-primary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Explainability Factor Breakdown (Transparent Scoring)
            </h3>
            <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginBottom: '14px', lineHeight: 1.5 }}>
              {selectedWO.severity_breakdown.explanation}
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px', textAlign: 'center' }}>
              <div style={{ background: 'var(--color-surface-subtle)', padding: '12px 10px', borderRadius: '8px', border: '1px solid var(--color-border-subtle)' }}>
                <span style={{ fontSize: '10px', color: 'var(--color-text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Base Severity</span>
                <strong style={{ display: 'block', fontSize: '16px', color: '#ef4444', marginTop: '2px' }}>+{selectedWO.severity_breakdown.severity_weight}</strong>
              </div>
              <div style={{ background: 'var(--color-surface-subtle)', padding: '12px 10px', borderRadius: '8px', border: '1px solid var(--color-border-subtle)' }}>
                <span style={{ fontSize: '10px', color: 'var(--color-text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Recurrence</span>
                <strong style={{ display: 'block', fontSize: '16px', color: 'var(--color-accent)', marginTop: '2px' }}>+{selectedWO.severity_breakdown.recurrence_weight}</strong>
              </div>
              <div style={{ background: 'var(--color-surface-subtle)', padding: '12px 10px', borderRadius: '8px', border: '1px solid var(--color-border-subtle)' }}>
                <span style={{ fontSize: '10px', color: 'var(--color-text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Corridor Context</span>
                <strong style={{ display: 'block', fontSize: '16px', color: '#818cf8', marginTop: '2px' }}>+{selectedWO.severity_breakdown.context_weight}</strong>
              </div>
              <div style={{ background: 'var(--color-surface-subtle)', padding: '12px 10px', borderRadius: '8px', border: '1px solid var(--color-border-subtle)' }}>
                <span style={{ fontSize: '10px', color: 'var(--color-text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Confidence</span>
                <strong style={{ display: 'block', fontSize: '16px', color: '#facc15', marginTop: '2px' }}>+{selectedWO.severity_breakdown.confidence_weight}</strong>
              </div>
            </div>
          </div>

          {/* Engineer Actions (Protected by RBAC) */}
          <div style={{
            background: 'var(--color-surface-elevated)',
            border: '1px solid var(--color-border-default)',
            borderRadius: 'var(--radius-md)',
            padding: '18px',
            display: 'flex',
            flexDirection: 'column',
            gap: '14px',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <UserCheck size={18} style={{ color: 'var(--color-accent)' }} />
                <span style={{ fontSize: '13px', fontWeight: '800', color: 'var(--color-text-primary)' }}>
                  Engineer Operational Workflow (RBAC Protected)
                </span>
              </div>
              <span style={{ fontSize: '11px', color: 'var(--color-text-secondary)' }}>
                Current User: <b style={{ color: 'var(--color-accent)' }}>{currentRole.toUpperCase()}</b>
              </span>
            </div>

            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
              <button
                id="btn-approve-wo"
                onClick={() => handleAction('assigned', 'PWD Maintenance Crew - Division 1')}
                disabled={actionLoading}
                style={{
                  background: 'linear-gradient(135deg, #38bdf8, #0284c7)',
                  color: '#080d14',
                  border: 'none',
                  padding: '10px 20px',
                  borderRadius: '8px',
                  fontWeight: '800',
                  fontSize: '12px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  boxShadow: '0 4px 12px rgba(56, 189, 248, 0.3)',
                  transition: 'all var(--transition-fast)'
                }}
              >
                <Check size={16} />
                <span>Approve & Assign to Crew</span>
              </button>

              <button
                id="btn-close-wo"
                onClick={() => handleAction('completed')}
                disabled={actionLoading}
                style={{
                  background: 'rgba(16, 185, 129, 0.12)',
                  color: '#10b981',
                  border: '1px solid rgba(16, 185, 129, 0.35)',
                  padding: '10px 20px',
                  borderRadius: '8px',
                  fontWeight: '800',
                  fontSize: '12px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  transition: 'all var(--transition-fast)'
                }}
              >
                <CheckCircle2 size={16} />
                <span>Mark Repaired & Close</span>
              </button>
            </div>

            {(currentRole === 'viewer' || currentRole === 'police') && (
              <div style={{
                fontSize: '11px',
                color: '#facc15',
                background: 'rgba(250, 204, 21, 0.1)',
                padding: '8px 12px',
                borderRadius: '6px',
                border: '1px solid rgba(250, 204, 21, 0.3)',
              }}>
                Notice: You are in <b>{currentRole.toUpperCase()}</b> mode. Clicking action buttons will enforce RBAC access restrictions.
              </div>
            )}
          </div>

          {/* Audit History for this Work Order */}
          <div>
            <h4 style={{ fontSize: '12px', fontWeight: '700', color: 'var(--color-text-muted)', textTransform: 'uppercase', marginBottom: '8px', letterSpacing: '0.04em' }}>
              Work Order Audit Trail
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {selectedWO.history.map((h, i) => (
                <div key={i} style={{
                  background: 'var(--color-surface-elevated)',
                  border: '1px solid var(--color-border-subtle)',
                  borderRadius: '8px',
                  padding: '10px 14px',
                  fontSize: '12px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}>
                  <div>
                    <strong style={{ color: 'var(--color-text-primary)' }}>{h.action}</strong>
                    <span style={{ color: 'var(--color-text-secondary)', marginLeft: '8px', fontSize: '11px' }}>by {h.username} ({h.role})</span>
                    {h.comment && <div style={{ color: 'var(--color-text-muted)', marginTop: '2px', fontSize: '11px' }}>"{h.comment}"</div>}
                  </div>
                  <span style={{ color: 'var(--color-text-muted)', fontSize: '11px', fontVariantNumeric: 'tabular-nums' }}>
                    {new Date(h.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>
      ) : (
        <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--color-text-muted)' }}>
          Select a work order from the queue to view details.
        </div>
      )}

    </div>
  );
}
