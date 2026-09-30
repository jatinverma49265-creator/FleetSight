import React from 'react';
import { 
  Bus, 
  MapPin, 
  ClipboardList, 
  Activity, 
  ShieldCheck, 
  RefreshCw, 
  UserCheck, 
  AlertTriangle 
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, currentRole, setCurrentRole, lastUpdated, onRefresh, isRefreshing }) {
  const roles = [
    { id: 'engineer', label: 'PWD Engineer', color: '#10b981' },
    { id: 'admin', label: 'City Admin', color: '#00d2b4' },
    { id: 'police', label: 'Traffic Police', color: '#3b82f6' },
    { id: 'viewer', label: 'Public Viewer', color: '#889ba8' },
  ];

  const tabs = [
    { id: 'map', label: 'GIS Live Map', icon: MapPin },
    { id: 'work_orders', label: 'Work Orders', icon: ClipboardList },
    { id: 'traffic', label: 'Traffic Heatmap', icon: Activity },
    { id: 'audit', label: 'Audit Trail', icon: ShieldCheck },
  ];

  return (
    <header style={{
      background: 'rgba(10, 20, 29, 0.95)',
      backdropFilter: 'blur(16px)',
      borderBottom: '1px solid var(--border-subtle)',
      padding: '0 24px',
      position: 'sticky',
      top: 0,
      zIndex: 1000,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '68px', gap: '20px' }}>
        
        {/* Brand & Bus sensing badge */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            background: 'linear-gradient(135deg, rgba(0, 210, 180, 0.15), rgba(14, 25, 35, 0.8))',
            padding: '6px 12px',
            borderRadius: '8px',
            border: '1px solid rgba(0, 210, 180, 0.3)'
          }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '6px',
              background: 'var(--brand-teal)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#070d13',
              fontWeight: '800',
              fontSize: '16px'
            }}>
              <Bus size={18} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '15px', fontWeight: '800', letterSpacing: '-0.02em', color: '#fff' }}>FleetSight</span>
                <span className="badge-simulated">SIMULATED DATA</span>
              </div>
              <span style={{ fontSize: '10px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                SIH26124 · Jaipur Mobile Sensing
              </span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
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
                  padding: '8px 16px',
                  borderRadius: '8px',
                  background: isActive ? 'rgba(0, 210, 180, 0.12)' : 'transparent',
                  border: isActive ? '1px solid rgba(0, 210, 180, 0.4)' : '1px solid transparent',
                  color: isActive ? 'var(--brand-teal)' : 'var(--text-muted)',
                  fontWeight: isActive ? '700' : '500',
                  fontSize: '13px',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
              >
                <Icon size={16} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Right side: Role Switcher & Live Polling */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          
          {/* Live Sync Status */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', color: 'var(--text-muted)' }}>
            <button
              id="manual-refresh-btn"
              onClick={onRefresh}
              disabled={isRefreshing}
              title="Refresh live state from backend"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-muted)',
                padding: '5px 9px',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '11px',
              }}
            >
              <RefreshCw size={12} className={isRefreshing ? 'animate-spin' : ''} style={{ animation: isRefreshing ? 'spin 1s linear infinite' : 'none' }} />
              <span>{isRefreshing ? 'Syncing...' : 'Sync'}</span>
            </button>
            <span>{lastUpdated ? lastUpdated.toLocaleTimeString() : 'Live'}</span>
          </div>

          {/* Role Switcher */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            background: 'rgba(255,255,255,0.03)',
            padding: '4px 10px',
            borderRadius: '8px',
            border: '1px solid var(--border-subtle)',
          }}>
            <UserCheck size={14} style={{ color: 'var(--brand-teal)' }} />
            <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontWeight: '600' }}>ROLE:</span>
            <select
              id="role-select"
              value={currentRole}
              onChange={(e) => setCurrentRole(e.target.value)}
              style={{
                background: 'transparent',
                color: '#fff',
                border: 'none',
                fontWeight: '700',
                fontSize: '12px',
                cursor: 'pointer',
                outline: 'none',
              }}
            >
              {roles.map((r) => (
                <option key={r.id} value={r.id} style={{ background: '#0e1923', color: '#fff' }}>
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
