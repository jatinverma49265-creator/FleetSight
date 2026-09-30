import React from 'react';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid, 
  BarChart, 
  Bar, 
  Legend 
} from 'recharts';
import { Activity, Car, Bus, Truck, Bike } from 'lucide-react';

export default function TrafficView({ trafficData }) {
  if (!trafficData) return null;

  const { corridor_name, total_vehicles, time_series, segments } = trafficData;

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '20px',
      margin: '20px 24px',
    }}>
      
      {/* Top Banner */}
      <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Activity size={20} style={{ color: 'var(--brand-teal)' }} />
            <h2 style={{ fontSize: '18px', fontWeight: '800', color: '#fff' }}>
              Corridor Traffic Congestion & 15-Minute Volume
            </h2>
            <span className="badge-simulated">SIMULATED</span>
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
            {corridor_name} · Edge AI vehicle detection telemetry
          </p>
        </div>

        <div style={{
          background: 'rgba(0, 210, 180, 0.1)',
          border: '1px solid rgba(0, 210, 180, 0.4)',
          padding: '8px 16px',
          borderRadius: '8px',
          textAlign: 'right',
        }}>
          <div style={{ fontSize: '24px', fontWeight: '800', color: 'var(--brand-teal)' }}>
            {total_vehicles}
          </div>
          <div style={{ fontSize: '9px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
            Total Vehicles (15m window)
          </div>
        </div>
      </div>

      {/* Grid: Corridor Time Series Chart & Segments Table */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: '20px' }}>
        
        {/* Chart */}
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: '700', color: '#fff' }}>
            Corridor Traffic Trend (15-Minute Intervals)
          </h3>
          <div style={{ width: '100%', height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={time_series} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorTonk" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00d2b4" stopOpacity={0.6}/>
                    <stop offset="95%" stopColor="#00d2b4" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorMI" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ff7a00" stopOpacity={0.6}/>
                    <stop offset="95%" stopColor="#ff7a00" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorJLN" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.6}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1c3244" />
                <XAxis dataKey="time" stroke="#889ba8" fontSize={11} />
                <YAxis stroke="#889ba8" fontSize={11} />
                <Tooltip
                  contentStyle={{ background: '#0e1923', borderColor: '#1c3244', borderRadius: '8px', fontSize: '11px' }}
                />
                <Area type="monotone" dataKey="tonk_road" name="Tonk Road" stroke="#00d2b4" fillOpacity={1} fill="url(#colorTonk)" />
                <Area type="monotone" dataKey="mi_road" name="MI Road" stroke="#ff7a00" fillOpacity={1} fill="url(#colorMI)" />
                <Area type="monotone" dataKey="jln_marg" name="JLN Marg" stroke="#3b82f6" fillOpacity={1} fill="url(#colorJLN)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Segment Congestion Heat List */}
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: '700', color: '#fff' }}>
            Road Segment Heat Metrics
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', overflowY: 'auto', maxHeight: '300px' }}>
            {segments.map((s) => {
              let badgeColor = '#10b981';
              if (s.congestion_level === 'severe') badgeColor = '#ef4444';
              else if (s.congestion_level === 'heavy') badgeColor = '#ff7a00';
              else if (s.congestion_level === 'moderate') badgeColor = '#eab308';

              return (
                <div key={s.segment_id} style={{
                  padding: '10px 12px',
                  background: 'rgba(255,255,255,0.02)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  fontSize: '11px',
                }}>
                  <div>
                    <b style={{ color: '#fff' }}>{s.road_name}</b>
                    <div style={{ color: 'var(--text-muted)', marginTop: '2px' }}>
                      Cars: {s.car_count} · Buses: {s.bus_count} · 2W: {s.two_wheeler_count}
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '14px', fontWeight: '800', color: '#fff' }}>
                      {s.vehicle_count}
                    </div>
                    <span style={{
                      background: `${badgeColor}22`,
                      color: badgeColor,
                      border: `1px solid ${badgeColor}55`,
                      padding: '2px 6px',
                      borderRadius: '4px',
                      fontSize: '9px',
                      fontWeight: '700',
                      textTransform: 'uppercase',
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
