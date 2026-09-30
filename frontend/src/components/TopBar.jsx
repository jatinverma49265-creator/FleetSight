import React from 'react';
import { RefreshCw, Search } from 'lucide-react';

export default function TopBar({ activeTab, lastUpdated, onRefresh, isRefreshing }) {
  const getTabTitle = () => {
    switch (activeTab) {
      case 'portal': return 'Public Information Portal & DPDP Charter';
      case 'dashboard': return 'Corridor Overview & Fleet Telemetry';
      case 'map': return 'GIS Live Corridor Map & Defect Tracking';
      case 'work_orders': return 'PWD Ranked Maintenance Work Orders';
      case 'traffic': return 'Corridor Traffic Congestion & Heatmap';
      case 'audit': return 'DPDP Act 2023 Security & Audit Trail';
      default: return 'Urban Infrastructure Monitoring';
    }
  };

  return (
    <header className="topbar-container">
      {/* Left: Context Breadcrumb */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', color: 'var(--c-slate-blue)', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
          <span>FleetSight</span>
          <span>/</span>
          <span style={{ color: 'var(--c-deep-navy)', fontWeight: '700' }}>{activeTab.replace('_', ' ')}</span>
        </div>
        <h2 style={{ fontSize: '17px', fontWeight: '800', color: 'var(--c-rich-navy)', margin: '2px 0 0 0' }}>
          {getTabTitle()}
        </h2>
      </div>

      {/* Right: Quick Search + Live Sync Status */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        
        {/* Search field */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          background: '#FFFFFF',
          border: '1px solid var(--color-border-default)',
          padding: '7px 14px',
          borderRadius: 'var(--radius-full)',
          width: '240px',
          boxShadow: 'var(--shadow-sm)',
          transition: 'all var(--transition-fast)'
        }}>
          <Search size={14} style={{ color: 'var(--c-slate-blue)' }} />
          <input
            type="text"
            placeholder="Search corridors, IDs..."
            aria-label="Search corridors or IDs"
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--c-rich-navy)',
              fontSize: '12px',
              outline: 'none',
              width: '100%',
              fontWeight: 500
            }}
          />
          <span style={{ fontSize: '10px', color: 'var(--c-slate-blue)', background: 'var(--color-surface-subtle)', padding: '1px 5px', borderRadius: '4px', fontWeight: 700, border: '1px solid var(--color-border-subtle)' }}>
            ⌘K
          </span>
        </div>

        {/* Sync Button */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', color: 'var(--c-slate-blue)' }}>
          <button
            id="manual-refresh-btn"
            onClick={onRefresh}
            disabled={isRefreshing}
            title="Refresh live telemetry state from backend"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: '#FFFFFF',
              border: '1px solid var(--c-soft-steel)',
              color: 'var(--c-deep-navy)',
              padding: '7px 13px',
              borderRadius: 'var(--radius-md)',
              cursor: 'pointer',
              fontSize: '11.5px',
              fontWeight: 700,
              boxShadow: 'var(--shadow-sm)',
              transition: 'all var(--transition-fast)',
            }}
          >
            <RefreshCw size={12} className={isRefreshing ? 'animate-spin' : ''} style={{ animation: isRefreshing ? 'spin 1s linear infinite' : 'none' }} />
            <span>{isRefreshing ? 'Syncing...' : 'Sync'}</span>
          </button>
          <span style={{ fontVariantNumeric: 'tabular-nums', fontSize: '11px', fontWeight: 600, color: 'var(--c-slate-blue)' }}>
            {lastUpdated ? lastUpdated.toLocaleTimeString() : 'Live'}
          </span>
        </div>

        {/* Simulated Badge */}
        <span className="badge-simulated">
          SIMULATED PILOT
        </span>

      </div>
    </header>
  );
}
