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
      color: 'var(--c-deep-navy)',
      bg: 'var(--color-surface-subtle)',
    },
    {
      id: 'kpi-km',
      label: 'Corridor Surveyed',
      value: `${kpis.km_surveyed ?? 48.6}`,
      unit: 'km surveyed today',
      icon: Route,
      color: 'var(--c-slate-blue)',
      bg: 'var(--color-surface-subtle)',
    },
    {
      id: 'kpi-defects',
      label: 'Defects Detected',
      value: kpis.defects_detected ?? 0,
      unit: `${kpis.defects_corroborated ?? 0} corroborated (2+ buses)`,
      icon: AlertOctagon,
      color: 'var(--color-safety-orange)',
      bg: 'rgba(234, 88, 12, 0.1)',
    },
    {
      id: 'kpi-work-orders',
      label: 'Work Orders',
      value: kpis.work_orders_created ?? 0,
      unit: `${kpis.work_orders_closed ?? 0} verified repaired`,
      icon: CheckCircle2,
      color: '#15803d',
      bg: 'rgba(21, 128, 61, 0.1)',
    },
    {
      id: 'kpi-latency',
      label: 'Median Latency',
      value: `${kpis.median_latency_seconds ?? 0.32}s`,
      unit: 'Target: <= 15s',
      icon: Zap,
      color: '#b45309',
      bg: 'rgba(180, 83, 9, 0.1)',
    },
    {
      id: 'kpi-bandwidth',
      label: 'Bandwidth Saved',
      value: `${kpis.bandwidth_saved_pct ?? 100}%`,
      unit: 'vs 720p raw video',
      icon: HardDrive,
      color: 'var(--c-deep-navy)',
      bg: 'var(--color-surface-subtle)',
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
              padding: '18px 20px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              gap: '10px',
              position: 'relative',
              overflow: 'hidden',
              background: '#FFFFFF'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '11px', color: 'var(--c-slate-blue)', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                {item.label}
              </span>
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                background: item.bg,
                border: '1px solid var(--color-border-subtle)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: item.color,
              }}>
                <Icon size={16} />
              </div>
            </div>

            <div>
              <div style={{
                fontSize: '28px',
                fontWeight: '800',
                color: 'var(--c-rich-navy)',
                fontFamily: 'var(--font-heading)',
                lineHeight: 1.1,
                letterSpacing: '-0.02em',
                fontVariantNumeric: 'tabular-nums'
              }}>
                {item.value}
              </div>
              <div style={{
                fontSize: '11px',
                color: 'var(--c-slate-blue)',
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
