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
    { id: 'engineer', label: 'PWD Engineer', color: '#10b981' },
    { id: 'admin', label: 'City Admin', color: '#38bdf8' },
    { id: 'police', label: 'Traffic Police', color: '#818cf8' },
    { id: 'viewer', label: 'Public Viewer', color: '#8A857D' },
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
          paddingBottom: '24px',
          borderBottom: '1px solid var(--color-border-subtle)',
          marginBottom: '20px'
        }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #6F452E, #54311D)',
            border: '1px solid #85624F',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#FEFEFE',
            boxShadow: '0 4px 12px rgba(84, 49, 29, 0.4)'
          }}>
            <Bus size={19} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '16px', fontWeight: '800', letterSpacing: '-0.02em', color: 'var(--color-text-primary)' }}>
                FleetSight
              </span>
            </div>
            <span style={{ fontSize: '10px', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: 600 }}>
              Mobile Urban Sensing
            </span>
          </div>
        </div>

        {/* Navigation Item List */}
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          <div style={{ fontSize: '10px', fontWeight: '700', color: 'var(--color-text-dim)', textTransform: 'uppercase', letterSpacing: '0.08em', padding: '0 12px 6px' }}>
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
                <Icon size={16} style={{ color: isActive ? 'var(--color-accent)' : 'var(--color-text-muted)' }} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Role Switcher & System Profile Footer */}
      <div style={{
        background: 'var(--color-surface-elevated)',
        border: '1px solid var(--color-border-default)',
        borderRadius: 'var(--radius-md)',
        padding: '12px 14px',
        display: 'flex',
        flexDirection: 'column',
        gap: '8px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <UserCheck size={14} style={{ color: 'var(--color-accent)' }} />
            <span style={{ fontSize: '10px', fontWeight: '700', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              ACTIVE ROLE
            </span>
          </div>
          <span className="badge-simulated" style={{ fontSize: '9px', padding: '1px 5px' }}>SIH26124</span>
        </div>

        <select
          id="role-select"
          aria-label="Select User Role"
          value={currentRole}
          onChange={(e) => setCurrentRole(e.target.value)}
          style={{
            background: 'var(--color-surface-subtle)',
            color: 'var(--color-text-primary)',
            border: '1px solid var(--color-border-default)',
            borderRadius: '6px',
            padding: '6px 8px',
            fontWeight: '700',
            fontSize: '12px',
            cursor: 'pointer',
            outline: 'none',
            width: '100%'
          }}
        >
          {roles.map((r) => (
            <option key={r.id} value={r.id} style={{ background: '#181512', color: '#FEFEFE' }}>
              {r.label}
            </option>
          ))}
        </select>
      </div>
    </aside>
  );
}
