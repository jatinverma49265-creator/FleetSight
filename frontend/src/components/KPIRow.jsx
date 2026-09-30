import React from 'react';
import { Bus, Route, CheckCircle2, AlertOctagon, Zap, HardDrive } from 'lucide-react';

export default function KPIRow({ kpis }) {
  if (!kpis) return null;

  const items = [
    {
      id: 'kpi-buses',
      label: 'Active Buses',
      value: kpis.buses_active ?? 3,
      unit: 'Units (RJ14 fleet)',
      icon: Bus,
      color: '#00d2b4',
      bg: 'rgba(0, 210, 180, 0.1)',
    },
    {
      id: 'kpi-km',
      label: 'Corridor Surveyed',
      value: `${kpis.km_surveyed ?? 48.6}`,
      unit: 'km today',
      icon: Route,
      color: '#3b82f6',
      bg: 'rgba(59, 130, 246, 0.1)',
    },
    {
      id: 'kpi-defects',
      label: 'Defects Detected',
      value: kpis.defects_detected ?? 0,
      unit: `${kpis.defects_corroborated ?? 0} corroborated (2+ buses)`,
      icon: AlertOctagon,
      color: '#ff7a00',
      bg: 'rgba(255, 122, 0, 0.1)',
    },
    {
      id: 'kpi-work-orders',
      label: 'Work Orders',
      value: kpis.work_orders_created ?? 0,
      unit: `${kpis.work_orders_closed ?? 0} closed / repaired`,
      icon: CheckCircle2,
      color: '#10b981',
      bg: 'rgba(16, 185, 129, 0.1)',
    },
    {
      id: 'kpi-latency',
      label: 'Median Latency',
      value: `${kpis.median_latency_seconds ?? 1.4}s`,
      unit: 'Target: <= 15s',
      icon: Zap,
      color: '#eab308',
      bg: 'rgba(234, 179, 8, 0.1)',
    },
    {
      id: 'kpi-bandwidth',
      label: 'Bandwidth Saved',
      value: `${kpis.bandwidth_saved_pct ?? 94.2}%`,
      unit: 'vs 720p raw stream',
      icon: HardDrive,
      color: '#a855f7',
      bg: 'rgba(168, 85, 247, 0.1)',
    },
  ];

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
      gap: '12px',
      margin: '18px 24px 0 24px',
    }}>
      {items.map((item) => {
        const Icon = item.icon;
        return (
          <div
            key={item.id}
            id={item.id}
            className="glass-panel glass-panel-hover"
            style={{
              padding: '14px 16px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              gap: '6px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                {item.label}
              </span>
              <div style={{
                width: '26px',
                height: '26px',
                borderRadius: '6px',
                background: item.bg,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: item.color,
              }}>
                <Icon size={14} />
              </div>
            </div>
            <div>
              <div style={{ fontSize: '24px', fontWeight: '800', color: '#fff', lineHeight: 1.1 }}>
                {item.value}
              </div>
              <div style={{ fontSize: '10px', color: 'var(--text-dim)', marginTop: '3px' }}>
                {item.unit}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
