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
      color: '#38bdf8',
      bg: 'rgba(56, 189, 248, 0.1)',
    },
    {
      id: 'kpi-km',
      label: 'Corridor Surveyed',
      value: `${kpis.km_surveyed ?? 48.6}`,
      unit: 'km surveyed today',
      icon: Route,
      color: '#818cf8',
      bg: 'rgba(129, 140, 248, 0.1)',
    },
    {
      id: 'kpi-defects',
      label: 'Defects Detected',
      value: kpis.defects_detected ?? 0,
      unit: `${kpis.defects_corroborated ?? 0} corroborated (2+ buses)`,
      icon: AlertOctagon,
      color: 'var(--color-safety-orange)',
      bg: 'rgba(249, 115, 22, 0.1)',
    },
    {
      id: 'kpi-work-orders',
      label: 'Work Orders',
      value: kpis.work_orders_created ?? 0,
      unit: `${kpis.work_orders_closed ?? 0} verified repaired`,
      icon: CheckCircle2,
      color: '#10b981',
      bg: 'rgba(16, 185, 129, 0.1)',
    },
    {
      id: 'kpi-latency',
      label: 'Median Latency',
      value: `${kpis.median_latency_seconds ?? 0.32}s`,
      unit: 'Target: <= 15s',
      icon: Zap,
      color: '#facc15',
      bg: 'rgba(250, 204, 21, 0.1)',
    },
    {
      id: 'kpi-bandwidth',
      label: 'Bandwidth Saved',
      value: `${kpis.bandwidth_saved_pct ?? 100}%`,
      unit: 'vs 720p raw video',
      icon: HardDrive,
      color: '#38bdf8',
      bg: 'rgba(56, 189, 248, 0.1)',
    },
  ];

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(190px, 1fr))',
      gap: '16px',
      margin: '20px 28px 0 28px',
    }}>
      {items.map((item) => {
        const Icon = item.icon;
        return (
          <div
            key={item.id}
            id={item.id}
            className="glass-panel glass-panel-hover"
            style={{
              padding: '16px 18px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              gap: '10px',
              position: 'relative',
              overflow: 'hidden'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '11px', color: 'var(--color-text-muted)', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                {item.label}
              </span>
              <div style={{
                width: '30px',
                height: '30px',
                borderRadius: '8px',
                background: item.bg,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: item.color,
              }}>
                <Icon size={15} />
              </div>
            </div>

            <div>
              <div style={{
                fontSize: '24px',
                fontWeight: '800',
                color: 'var(--color-text-primary)',
                fontFamily: 'var(--font-heading)',
                lineHeight: 1.1,
                letterSpacing: '-0.02em',
                fontVariantNumeric: 'tabular-nums'
              }}>
                {item.value}
              </div>
              <div style={{
                fontSize: '11px',
                color: 'var(--color-text-secondary)',
                marginTop: '4px',
                fontWeight: '500'
              }}>
                {item.unit}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
