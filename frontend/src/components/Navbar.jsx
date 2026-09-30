import React from 'react';
import { 
  Bus, 
  MapPin, 
  ClipboardList, 
  Activity, 
  ShieldCheck, 
  RefreshCw, 
  UserCheck, 
  Globe
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, currentRole, setCurrentRole, lastUpdated, onRefresh, isRefreshing }) {
  const roles = [
    { id: 'engineer', label: 'PWD Engineer', color: '#10b981' },
    { id: 'admin', label: 'City Admin', color: '#38bdf8' },
    { id: 'police', label: 'Traffic Police', color: '#818cf8' },
    { id: 'viewer', label: 'Public Viewer', color: '#94a3b8' },
  ];

  const tabs = [
    { id: 'portal', label: 'Public Portal & DPDP', icon: Globe },
    { id: 'map', label: 'GIS Live Map', icon: MapPin },
    { id: 'work_orders', label: 'Work Orders', icon: ClipboardList },
    { id: 'traffic', label: 'Traffic Heatmap', icon: Activity },
    { id: 'audit', label: 'Audit Trail', icon: ShieldCheck },
  ];

  return (
    <header style={{
      background: 'rgba(8, 13, 20, 0.88)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid var(--color-border-subtle)',
      padding: '0 28px',
      position: 'sticky',
      top: 0,
      zIndex: 1000,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '66px', gap: '20px' }}>
        
        {/* Brand & Bus sensing badge */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            background: 'rgba(14, 23, 34, 0.9)',
            padding: '6px 14px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--color-border-default)',
            boxShadow: 'var(--shadow-sm)',
          }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #38bdf8, #0284c7)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#080d14',
              fontWeight: '800',
              boxShadow: '0 2px 10px rgba(56, 189, 248, 0.3)'
            }}>
              <Bus size={18} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '15px', fontWeight: '800', letterSpacing: '-0.02em', color: 'var(--color-text-primary)' }}>FleetSight</span>
                <span className="badge-simulated">SIMULATED DATA</span>
              </div>
              <span style={{ fontSize: '10px', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: 600 }}>
                SIH26124 · Jaipur Mobile Sensing
              </span>
            </div>
          </div>
        </div>

        {/* Segmented Pill Navigation Tabs */}
        <nav style={{
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          background: 'rgba(14, 23, 34, 0.7)',
          padding: '4px',
          borderRadius: 'var(--radius-lg)',
          border: '1px solid var(--color-border-subtle)',
        }}>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                id={`tab-btn-${tab.id}`}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '7px 15px',
                  borderRadius: '10px',
                  background: isActive ? 'rgba(56, 189, 248, 0.12)' : 'transparent',
                  border: isActive ? '1px solid rgba(56, 189, 248, 0.28)' : '1px solid transparent',
                  color: isActive ? '#f8fafc' : 'var(--color-text-secondary)',
                  fontWeight: isActive ? '700' : '500',
                  fontSize: '13px',
                  cursor: 'pointer',
                  transition: 'all var(--transition-fast)',
                }}
              >
                <Icon size={15} style={{ color: isActive ? 'var(--color-accent)' : 'var(--color-text-muted)' }} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Right side: Role Switcher & Live Polling */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          
          {/* Live Sync Status */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', color: 'var(--color-text-muted)' }}>
            <button
              id="manual-refresh-btn"
              onClick={onRefresh}
              disabled={isRefreshing}
              title="Refresh live state from backend"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
                background: 'rgba(14, 23, 34, 0.8)',
                border: '1px solid var(--color-border-default)',
                color: 'var(--color-text-secondary)',
                padding: '6px 11px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '11px',
                fontWeight: 600,
                transition: 'all var(--transition-fast)',
              }}
            >
              <RefreshCw size={12} className={isRefreshing ? 'animate-spin' : ''} style={{ animation: isRefreshing ? 'spin 1s linear infinite' : 'none' }} />
              <span>{isRefreshing ? 'Syncing...' : 'Sync'}</span>
            </button>
            <span style={{ fontVariantNumeric: 'tabular-nums' }}>{lastUpdated ? lastUpdated.toLocaleTimeString() : 'Live'}</span>
          </div>

          {/* Role Switcher Pill */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            background: 'rgba(14, 23, 34, 0.9)',
            padding: '5px 12px',
            borderRadius: '10px',
            border: '1px solid var(--color-border-default)',
            boxShadow: 'var(--shadow-sm)'
          }}>
            <UserCheck size={14} style={{ color: 'var(--color-accent)' }} />
            <span style={{ fontSize: '10px', color: 'var(--color-text-muted)', fontWeight: '700', letterSpacing: '0.05em' }}>ROLE</span>
            <select
              id="role-select"
              value={currentRole}
              onChange={(e) => setCurrentRole(e.target.value)}
              style={{
                background: 'transparent',
                color: '#f8fafc',
                border: 'none',
                fontWeight: '700',
                fontSize: '12px',
                cursor: 'pointer',
                outline: 'none',
              }}
            >
              {roles.map((r) => (
                <option key={r.id} value={r.id} style={{ background: '#0e1722', color: '#f8fafc' }}>
                  {r.label}
                </option>
              ))}
            </select>
          </div>

        </div>

      </div>
    </header>
  );
}
