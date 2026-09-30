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
  const defaultTraffic = {
    corridor_name: 'Jaipur Smart City Arterials (MI Road · Tonk Road · JLN Marg)',
    total_vehicles: 1240,
    time_series: [
      { time: '08:00', mi_road: 120, tonk_road: 180, jln_marg: 90 },
      { time: '09:00', mi_road: 240, tonk_road: 310, jln_marg: 190 },
      { time: '10:00', mi_road: 310, tonk_road: 420, jln_marg: 260 },
      { time: '11:00', mi_road: 280, tonk_road: 380, jln_marg: 220 },
      { time: '12:00', mi_road: 210, tonk_road: 290, jln_marg: 170 },
      { time: '13:00', mi_road: 190, tonk_road: 270, jln_marg: 150 },
      { time: '14:00', mi_road: 230, tonk_road: 320, jln_marg: 180 }
    ],
    segments: [
      { name: 'MI Road (Ajmeri Gate to Government Hostel)', density: 'high', vehicle_count: 420 },
      { name: 'Tonk Road (Rambagh Circle to Gandhi Nagar)', density: 'medium', vehicle_count: 360 },
      { name: 'JLN Marg (World Trade Park to OTS)', density: 'low', vehicle_count: 190 }
    ]
  };

  const data = trafficData || defaultTraffic;
  const { corridor_name, total_vehicles, time_series, segments } = data;

  return (
    <div className="animate-fade-in" style={{
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
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              background: 'var(--color-surface-subtle)',
              border: '1px solid var(--color-border-subtle)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--c-deep-navy)'
            }}>
              <Activity size={18} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <h2 style={{ fontSize: '17px', fontWeight: '800', color: 'var(--c-rich-navy)', margin: 0 }}>
                  Corridor Traffic Congestion & 15-Minute Volume
                </h2>
                <span className="badge-simulated">SIMULATED</span>
              </div>
              <p style={{ fontSize: '12px', color: 'var(--c-slate-blue)', marginTop: '2px', margin: 0, fontWeight: 500 }}>
                {corridor_name} · Edge AI vehicle detection telemetry
              </p>
            </div>
          </div>
        </div>

        <div style={{
          background: 'var(--color-surface-subtle)',
          border: '1px solid var(--color-border-default)',
          padding: '8px 18px',
          borderRadius: 'var(--radius-md)',
          textAlign: 'right',
          boxShadow: 'var(--shadow-sm)'
        }}>
          <div style={{ fontSize: '24px', fontWeight: '800', color: 'var(--c-deep-navy)', fontVariantNumeric: 'tabular-nums' }}>
            {total_vehicles}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--c-slate-blue)', textTransform: 'uppercase', fontWeight: '800', letterSpacing: '0.04em' }}>
            Total Vehicles (15m window)
          </div>
        </div>
      </div>

      {/* Grid: Corridor Time Series Chart & Segments Table */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: '20px' }}>
        
        {/* Chart Card */}
        <div className="glass-panel" style={{ padding: '22px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '14.5px', fontWeight: '800', color: 'var(--c-rich-navy)' }}>
              Corridor Traffic Trend (15-Minute Intervals)
            </h3>
            <span style={{ fontSize: '11px', color: 'var(--c-slate-blue)', fontWeight: 600 }}>Vehicles / interval</span>
          </div>
          
          <div style={{ width: '100%', height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={time_series} margin={{ top: 10, right: 15, left: -10, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorTonk" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#1B263B" stopOpacity={0.35}/>
                    <stop offset="95%" stopColor="#1B263B" stopOpacity={0.02}/>
                  </linearGradient>
                  <linearGradient id="colorMI" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#415A77" stopOpacity={0.30}/>
                    <stop offset="95%" stopColor="#415A77" stopOpacity={0.02}/>
                  </linearGradient>
                  <linearGradient id="colorJLN" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#778DA9" stopOpacity={0.25}/>
                    <stop offset="95%" stopColor="#778DA9" stopOpacity={0.02}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(119, 141, 169, 0.25)" vertical={false} />
                <XAxis dataKey="time" stroke="#415A77" fontSize={11} tickLine={false} />
                <YAxis stroke="#415A77" fontSize={11} tickLine={false} />
                <Tooltip
                  contentStyle={{ 
                    background: '#FFFFFF', 
                    borderColor: '#778DA9', 
                    borderRadius: '8px', 
                    fontSize: '11px', 
                    boxShadow: '0 4px 16px rgba(13, 27, 42, 0.12)',
                    color: '#0D1B2A'
                  }}
                />
                <Area type="monotone" dataKey="tonk_road" name="Tonk Road" stroke="#1B263B" strokeWidth={2.5} fillOpacity={1} fill="url(#colorTonk)" />
                <Area type="monotone" dataKey="mi_road" name="MI Road" stroke="#415A77" strokeWidth={2.5} fillOpacity={1} fill="url(#colorMI)" />
                <Area type="monotone" dataKey="jln_marg" name="JLN Marg" stroke="#778DA9" strokeWidth={2} fillOpacity={1} fill="url(#colorJLN)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Segment Breakdown */}
        <div className="glass-panel" style={{ padding: '22px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '14.5px', fontWeight: '800', color: 'var(--c-rich-navy)' }}>
              Corridor Segment Density
            </h3>
            <span style={{ fontSize: '11px', color: 'var(--c-slate-blue)', fontWeight: 600 }}>Real-time Edge Aggregates</span>
          </div>

          <div tabIndex={0} aria-label="Corridor Segment Density Table" style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflowY: 'auto', maxHeight: '300px', outline: 'none' }}>
            {segments.map((seg, i) => {
              const roadName = seg.road_name || seg.name || 'Jaipur Arterial';
              const congestion = (seg.congestion_level || seg.density || 'moderate').toLowerCase();
              return (
                <div key={i} className="glass-panel-hover" style={{
                  background: '#FFFFFF',
                  border: '1px solid var(--color-border-default)',
                  borderRadius: '8px',
                  padding: '12px 14px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  boxShadow: 'var(--shadow-sm)'
                }}>
                  <div>
                    <strong style={{ fontSize: '12.5px', color: 'var(--c-rich-navy)' }}>{roadName}</strong>
                    <div style={{ fontSize: '11px', color: 'var(--c-slate-blue)', marginTop: '2px' }}>
                      Congestion Index: <b style={{ color: congestion === 'severe' || congestion === 'high' ? '#b91c1c' : congestion === 'heavy' || congestion === 'medium' ? '#b45309' : '#15803d' }}>{congestion.toUpperCase()}</b>
                    </div>
                  </div>

                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '16px', fontWeight: '800', color: 'var(--c-deep-navy)', fontVariantNumeric: 'tabular-nums' }}>
                      {seg.vehicle_count}
                    </div>
                    <div style={{ fontSize: '10px', color: 'var(--c-slate-blue)', fontWeight: 600 }}>vehicles / 15m</div>
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
