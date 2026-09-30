import React from 'react';
import { 
  Bus, 
  MapPin, 
  ClipboardList, 
  Activity, 
  ShieldCheck, 
  Globe, 
  LayoutDashboard,
  UserCheck
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, currentRole, setCurrentRole }) {
  const roles = [
    { id: 'engineer', label: 'PWD Engineer', color: '#15803d' },
    { id: 'admin', label: 'City Admin', color: '#1B263B' },
    { id: 'police', label: 'Traffic Police', color: '#415A77' },
    { id: 'viewer', label: 'Public Viewer', color: '#778DA9' },
  ];

  const tabs = [
    { id: 'portal', label: 'Public Portal & DPDP', icon: Globe },
    { id: 'dashboard', label: 'Overview & Insights', icon: LayoutDashboard },
    { id: 'map', label: 'GIS Live Map', icon: MapPin },
    { id: 'work_orders', label: 'Work Orders', icon: ClipboardList },
    { id: 'traffic', label: 'Traffic Heatmap', icon: Activity },
    { id: 'audit', label: 'Audit Trail', icon: ShieldCheck },
  ];

  return (
    <aside className="sidebar-container" aria-label="Main Navigation">
      {/* Brand & Logo Header */}
      <div>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          paddingBottom: '22px',
          borderBottom: '1px solid var(--color-border-default)',
          marginBottom: '20px'
        }}>
          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, var(--c-deep-navy), var(--c-rich-navy))',
            border: '1px solid var(--c-slate-blue)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#FFFFFF',
            boxShadow: '0 4px 12px rgba(13, 27, 42, 0.18)'
          }}>
            <Bus size={20} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '17px', fontWeight: '800', letterSpacing: '-0.02em', color: 'var(--c-rich-navy)' }}>
                FleetSight
              </span>
            </div>
            <span style={{ fontSize: '10px', color: 'var(--c-slate-blue)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: 600 }}>
              Mobile Urban Sensing
            </span>
          </div>
        </div>

        {/* Navigation Item List */}
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          <div style={{ fontSize: '10px', fontWeight: '700', color: 'var(--c-slate-blue)', textTransform: 'uppercase', letterSpacing: '0.08em', padding: '0 12px 6px' }}>
            Navigation
          </div>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                id={`tab-btn-${tab.id}`}
                onClick={() => setActiveTab(tab.id)}
                className={`sidebar-nav-btn ${isActive ? 'active' : ''}`}
              >
                <Icon size={16} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Role Switcher & System Profile Footer */}
      <div style={{
        background: 'var(--color-surface-subtle)',
        border: '1px solid var(--color-border-default)',
        borderRadius: 'var(--radius-md)',
        padding: '12px 14px',
        display: 'flex',
        flexDirection: 'column',
        gap: '8px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <UserCheck size={14} style={{ color: 'var(--c-deep-navy)' }} />
            <span style={{ fontSize: '10px', fontWeight: '700', color: 'var(--c-slate-blue)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              ACTIVE ROLE
            </span>
          </div>
          <span className="badge-simulated" style={{ fontSize: '9px', padding: '1px 6px' }}>ACTIVE</span>
        </div>

        <select
          id="role-select"
          aria-label="Select User Role"
          value={currentRole}
          onChange={(e) => setCurrentRole(e.target.value)}
          style={{
            background: '#FFFFFF',
            color: 'var(--c-rich-navy)',
            border: '1px solid var(--c-soft-steel)',
            borderRadius: '6px',
            padding: '7px 10px',
            fontWeight: '700',
            fontSize: '12px',
            cursor: 'pointer',
            outline: 'none',
            width: '100%',
            transition: 'border-color var(--transition-fast)'
          }}
        >
          {roles.map((r) => (
            <option key={r.id} value={r.id} style={{ background: '#FFFFFF', color: '#0D1B2A' }}>
              {r.label}
            </option>
          ))}
        </select>
      </div>
    </aside>
  );
}
