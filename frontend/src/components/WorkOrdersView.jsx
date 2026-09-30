import React, { useState } from 'react';
import { 
  ClipboardList, 
  CheckCircle2, 
  UserCheck, 
  Clock, 
  ShieldAlert, 
  ArrowRight, 
  AlertOctagon, 
  Sparkles, 
  Check, 
  X 
} from 'lucide-react';
import { updateWorkOrder } from '../api';

export default function WorkOrdersView({ workOrders, currentRole, onRefresh, onTriggerDenialModal }) {
  const [selectedWO, setSelectedWO] = useState(workOrders[0] || null);
  const [assigneeInput, setAssigneeInput] = useState('');
  const [commentInput, setCommentInput] = useState('');
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
          comment: commentInput || `Work order updated to ${status} by ${currentRole}.`,
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
      margin: '20px 24px',
      minHeight: 'calc(100vh - 220px)',
    }}>
      
      {/* Left Column: Ranked Work Orders List */}
      <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: '800', color: '#fff' }}>
              Ranked Work-Order Queue
            </h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Prioritised candidates generated via 2+ bus corroboration
            </p>
          </div>
          <span className="badge-simulated">SIMULATED</span>
        </div>

        {/* Work Order Cards */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflowY: 'auto', maxHeight: 'calc(100vh - 300px)' }}>
          {workOrders.map((wo) => {
            const isSelected = selectedWO?.work_order_id === wo.work_order_id;
            let statusColor = '#f59e0b';
            if (wo.status === 'assigned' || wo.status === 'in_progress') statusColor = '#3b82f6';
            else if (wo.status === 'completed' || wo.status === 'closed') statusColor = '#10b981';

            return (
              <div
                key={wo.work_order_id}
                id={`wo-card-${wo.work_order_id}`}
                onClick={() => setSelectedWO(wo)}
                className="glass-panel-hover"
                style={{
                  padding: '14px 16px',
                  borderRadius: '8px',
                  background: isSelected ? 'rgba(0, 210, 180, 0.12)' : 'rgba(255,255,255,0.02)',
                  border: isSelected ? '1px solid var(--brand-teal)' : '1px solid var(--border-subtle)',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '12px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                  <div style={{
                    width: '42px',
                    height: '42px',
                    borderRadius: '8px',
                    background: 'rgba(0,0,0,0.4)',
                    border: '1px solid var(--border-subtle)',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}>
                    <span style={{ fontSize: '15px', fontWeight: '800', color: 'var(--brand-teal)' }}>
                      {wo.priority_score}
                    </span>
                    <span style={{ fontSize: '8px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
                      SCORE
                    </span>
                  </div>

                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <b style={{ fontSize: '13px', color: '#fff' }}>{wo.title}</b>
                    </div>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>
                      {wo.road_segment} · <b>{wo.observation_count} bus passes</b>
                    </div>
                  </div>
                </div>

                <div style={{ textAlign: 'right' }}>
                  <span style={{
                    background: `${statusColor}22`,
                    color: statusColor,
                    border: `1px solid ${statusColor}55`,
                    padding: '3px 8px',
                    borderRadius: '4px',
                    fontSize: '10px',
                    fontWeight: '700',
                    textTransform: 'uppercase',
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
                <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--brand-teal)', fontWeight: '700' }}>
                  {selectedWO.work_order_id}
                </span>
                <span style={{
                  background: 'rgba(16, 185, 129, 0.15)',
                  color: '#10b981',
                  border: '1px solid rgba(16, 185, 129, 0.4)',
                  padding: '2px 8px',
                  borderRadius: '4px',
                  fontSize: '10px',
                  fontWeight: '700',
                }}>
                  CORROBORATED BY {selectedWO.corroborating_buses.length || 2} BUSES
                </span>
              </div>
              <h1 style={{ fontSize: '22px', fontWeight: '800', color: '#fff' }}>
                {selectedWO.title}
              </h1>
              <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
                {selectedWO.description}
              </p>
            </div>

            <div style={{
              background: 'rgba(0, 210, 180, 0.1)',
              border: '1px solid rgba(0, 210, 180, 0.4)',
              padding: '10px 18px',
              borderRadius: '10px',
              textAlign: 'center',
            }}>
              <div style={{ fontSize: '28px', fontWeight: '800', color: 'var(--brand-teal)' }}>
                {selectedWO.priority_score}
              </div>
              <div style={{ fontSize: '9px', color: 'var(--text-dim)', textTransform: 'uppercase', fontWeight: '700' }}>
                Priority Score
              </div>
            </div>
          </div>

          {actionSuccess && (
            <div style={{
              background: 'rgba(16, 185, 129, 0.15)',
              border: '1px solid #10b981',
              color: '#10b981',
              padding: '10px 14px',
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
            background: 'rgba(255,255,255,0.02)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '10px',
            padding: '16px',
          }}>
            <h3 style={{ fontSize: '13px', fontWeight: '700', color: '#fff', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Explainability Factor Breakdown (Transparent Scoring)
            </h3>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '14px' }}>
              {selectedWO.severity_breakdown.explanation}
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px', textAlign: 'center' }}>
              <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-subtle)' }}>
                <span style={{ fontSize: '10px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>Base Severity</span>
                <b style={{ display: 'block', fontSize: '16px', color: '#ef4444', marginTop: '2px' }}>+{selectedWO.severity_breakdown.severity_weight}</b>
              </div>
              <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-subtle)' }}>
                <span style={{ fontSize: '10px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>Recurrence</span>
                <b style={{ display: 'block', fontSize: '16px', color: 'var(--brand-teal)', marginTop: '2px' }}>+{selectedWO.severity_breakdown.recurrence_weight}</b>
              </div>
              <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-subtle)' }}>
                <span style={{ fontSize: '10px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>Corridor Context</span>
                <b style={{ display: 'block', fontSize: '16px', color: '#3b82f6', marginTop: '2px' }}>+{selectedWO.severity_breakdown.context_weight}</b>
              </div>
              <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-subtle)' }}>
                <span style={{ fontSize: '10px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>Confidence</span>
                <b style={{ display: 'block', fontSize: '16px', color: '#eab308', marginTop: '2px' }}>+{selectedWO.severity_breakdown.confidence_weight}</b>
              </div>
            </div>
          </div>

          {/* Engineer Actions (Protected by RBAC) */}
          <div style={{
            background: 'rgba(0, 210, 180, 0.05)',
            border: '1px solid rgba(0, 210, 180, 0.3)',
            borderRadius: '10px',
            padding: '18px',
            display: 'flex',
            flexDirection: 'column',
            gap: '14px',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <UserCheck size={18} style={{ color: 'var(--brand-teal)' }} />
                <span style={{ fontSize: '13px', fontWeight: '800', color: '#fff' }}>
                  Engineer Operational Workflow (RBAC Protected)
                </span>
              </div>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                Current User: <b>{currentRole.toUpperCase()}</b>
              </span>
            </div>

            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
              <button
                id="btn-approve-wo"
                onClick={() => handleAction('assigned', 'PWD Maintenance Crew - Division 1')}
                disabled={actionLoading}
                style={{
                  background: 'var(--brand-teal)',
                  color: '#070d13',
                  border: 'none',
                  padding: '10px 18px',
                  borderRadius: '6px',
                  fontWeight: '800',
                  fontSize: '12px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
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
                  background: 'rgba(16, 185, 129, 0.15)',
                  color: '#10b981',
                  border: '1px solid #10b981',
                  padding: '10px 18px',
                  borderRadius: '6px',
                  fontWeight: '800',
                  fontSize: '12px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                }}
              >
                <CheckCircle2 size={16} />
                <span>Mark Repaired & Close</span>
              </button>
            </div>

            {(currentRole === 'viewer' || currentRole === 'police') && (
              <div style={{
                fontSize: '11px',
                color: '#f59e0b',
                background: 'rgba(245, 158, 11, 0.1)',
                padding: '8px 12px',
                borderRadius: '6px',
                border: '1px solid rgba(245, 158, 11, 0.3)',
              }}>
                Notice: You are in <b>{currentRole.toUpperCase()}</b> mode. Clicking action buttons will enforce RBAC access restrictions.
              </div>
            )}
          </div>

          {/* Audit History for this Work Order */}
          <div>
            <h4 style={{ fontSize: '12px', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px' }}>
              Work Order Audit Trail
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {selectedWO.history.map((h, i) => (
                <div key={i} style={{
                  background: 'rgba(255,255,255,0.02)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '6px',
                  padding: '8px 12px',
                  fontSize: '11px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}>
                  <div>
                    <b style={{ color: '#fff' }}>{h.action}</b>
                    <span style={{ color: 'var(--text-muted)', marginLeft: '8px' }}>by {h.username} ({h.role})</span>
                    {h.comment && <div style={{ color: 'var(--text-dim)', marginTop: '2px' }}>"{h.comment}"</div>}
                  </div>
                  <span style={{ color: 'var(--text-dim)', fontSize: '10px' }}>
                    {new Date(h.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>
      ) : (
        <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
          Select a work order from the queue to view details.
        </div>
      )}

    </div>
  );
}
