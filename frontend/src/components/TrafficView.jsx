import React from 'react';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid 
} from 'recharts';
import { Activity, Car, Bus } from 'lucide-react';

export default function TrafficView({ trafficData }) {
  if (!trafficData) return null;

  const { corridor_name, total_vehicles, time_series, segments } = trafficData;

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '20px',
      margin: '20px 28px',
    }}>
      
      {/* Top Banner */}
      <div className="glass-panel" style={{ padding: '20px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              background: 'rgba(56, 189, 248, 0.12)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--color-accent)'
            }}>
              <Activity size={18} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <h2 style={{ fontSize: '17px', fontWeight: '800', color: 'var(--color-text-primary)', margin: 0 }}>
                  Corridor Traffic Congestion & 15-Minute Volume
                </h2>
                <span className="badge-simulated">SIMULATED</span>
              </div>
              <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '2px', margin: 0 }}>
                {corridor_name} · Edge AI vehicle detection telemetry
              </p>
            </div>
          </div>
        </div>

        <div style={{
          background: 'var(--color-surface-elevated)',
          border: '1px solid var(--color-border-default)',
          padding: '8px 18px',
          borderRadius: 'var(--radius-md)',
          textAlign: 'right',
          boxShadow: 'var(--shadow-sm)'
        }}>
          <div style={{ fontSize: '22px', fontWeight: '800', color: 'var(--color-accent)', fontVariantNumeric: 'tabular-nums' }}>
            {total_vehicles}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--color-text-muted)', textTransform: 'uppercase', fontWeight: '700', letterSpacing: '0.04em' }}>
            Total Vehicles (15m window)
          </div>
        </div>
      </div>

      {/* Grid: Corridor Time Series Chart & Segments Table */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: '20px' }}>
        
        {/* Chart Card */}
        <div className="glass-panel" style={{ padding: '22px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--color-text-primary)' }}>
              Corridor Traffic Trend (15-Minute Intervals)
            </h3>
            <span style={{ fontSize: '11px', color: 'var(--color-text-muted)', fontWeight: 600 }}>Vehicles / interval</span>
          </div>
          
          <div style={{ width: '100%', height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={time_series} margin={{ top: 10, right: 15, left: -10, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorTonk" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#38bdf8" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorMI" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f97316" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorJLN" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00d2b4" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#00d2b4" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" vertical={false} />
                <XAxis dataKey="time" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip
                  contentStyle={{ 
                    background: '#142130', 
                    borderColor: 'rgba(148, 163, 184, 0.25)', 
                    borderRadius: '8px', 
                    fontSize: '11px', 
                    boxShadow: '0 10px 25px rgba(0,0,0,0.5)',
                    color: '#f8fafc'
                  }}
                />
                <Area type="monotone" dataKey="tonk_road" name="Tonk Road" stroke="#38bdf8" strokeWidth={2} fillOpacity={1} fill="url(#colorTonk)" />
                <Area type="monotone" dataKey="mi_road" name="MI Road" stroke="#f97316" strokeWidth={2} fillOpacity={1} fill="url(#colorMI)" />
                <Area type="monotone" dataKey="jln_marg" name="JLN Marg" stroke="#00d2b4" strokeWidth={2} fillOpacity={1} fill="url(#colorJLN)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Segment Congestion Heat List */}
        <div className="glass-panel" style={{ padding: '22px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--color-text-primary)' }}>
            Road Segment Heat Metrics
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflowY: 'auto', maxHeight: '300px' }}>
            {segments.map((s) => {
              let badgeColor = '#10b981';
              if (s.congestion_level === 'severe') badgeColor = '#ef4444';
              else if (s.congestion_level === 'heavy') badgeColor = '#f97316';
              else if (s.congestion_level === 'moderate') badgeColor = '#facc15';

              return (
                <div key={s.segment_id} style={{
                  padding: '12px 14px',
                  background: 'var(--color-surface-elevated)',
                  border: '1px solid var(--color-border-default)',
                  borderRadius: 'var(--radius-md)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  fontSize: '12px',
                  transition: 'border-color var(--transition-fast)'
                }}>
                  <div>
                    <strong style={{ color: 'var(--color-text-primary)' }}>{s.road_name}</strong>
                    <div style={{ color: 'var(--color-text-secondary)', marginTop: '2px', fontSize: '11px' }}>
                      Cars: {s.car_count} · Buses: {s.bus_count} · 2W: {s.two_wheeler_count}
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '15px', fontWeight: '800', color: 'var(--color-text-primary)', fontVariantNumeric: 'tabular-nums' }}>
                      {s.vehicle_count}
                    </div>
                    <span style={{
                      background: `${badgeColor}18`,
                      color: badgeColor,
                      border: `1px solid ${badgeColor}40`,
                      padding: '2px 7px',
                      borderRadius: '4px',
                      fontSize: '9px',
                      fontWeight: '700',
                      textTransform: 'uppercase',
                      letterSpacing: '0.04em'
                    }}>
                      {s.congestion_level}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

      </div>

    </div>
  );
}
