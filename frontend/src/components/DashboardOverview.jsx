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
import { 
  Bus, 
  Route, 
  CheckCircle2, 
  AlertOctagon, 
  ArrowUpRight, 
  ShieldCheck, 
  MapPin, 
  Zap,
  Activity,
  HardDrive
} from 'lucide-react';

export default function DashboardOverview({ kpis, trafficData, issues, workOrders, onNavigateTab }) {
  const timeSeries = trafficData?.time_series || [];

  return (
    <div style={{ padding: '24px 32px 48px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* 1. Context Welcome Banner */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'var(--color-surface-card)',
        border: '1px solid var(--color-border-default)',
        borderRadius: 'var(--radius-lg)',
        padding: '20px 24px',
        boxShadow: 'var(--shadow-sm)'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--color-accent)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              SMART MOBILITY INTELLIGENCE
            </span>
            <span className="badge-simulated">JAIPUR PILOT</span>
          </div>
          <h1 style={{ fontSize: '22px', fontWeight: '800', color: 'var(--color-text-primary)', margin: 0 }}>
            Urban Road Health & Autonomous Fleet Sensing
          </h1>
          <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '4px', margin: 0 }}>
            3 Active Public Buses Surveying Arterial Routes (MI Road · Tonk Road · JLN Marg)
          </p>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={() => onNavigateTab('map')}
            style={{
              background: 'linear-gradient(135deg, #38bdf8, #0284c7)',
              color: '#080d14',
              border: 'none',
              padding: '10px 18px',
              borderRadius: 'var(--radius-md)',
              fontSize: '12px',
              fontWeight: '700',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              boxShadow: '0 4px 12px rgba(56, 189, 248, 0.35)',
              transition: 'all var(--transition-fast)'
            }}
          >
            <MapPin size={15} />
            <span>Open GIS Map</span>
            <ArrowUpRight size={14} />
          </button>
        </div>
      </div>

      {/* 2. KPI Summary Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
        
        {/* Active Buses */}
        <div id="kpi-buses" className="glass-panel glass-panel-hover" style={{ padding: '18px 20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: '12px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Active Buses
            </span>
            <div style={{ width: '28px', height: '28px', borderRadius: '6px', background: 'rgba(56, 189, 248, 0.1)', color: 'var(--color-accent)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Bus size={15} />
            </div>
          </div>
          <div>
            <div style={{ fontSize: '28px', fontWeight: '800', color: 'var(--color-text-primary)', fontVariantNumeric: 'tabular-nums' }}>
              {kpis?.buses_active ?? 3}
            </div>
            <div style={{ fontSize: '11px', color: 'var(--color-text-secondary)', marginTop: '2px', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <span style={{ color: '#10b981', fontWeight: '700' }}>+100% online</span>
              <span>· RJ14 Fleet Units</span>
            </div>
          </div>
        </div>

        {/* Surveyed Corridor */}
        <div className="glass-panel glass-panel-hover" style={{ padding: '18px 20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: '12px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Corridor Surveyed
            </span>
            <div style={{ width: '28px', height: '28px', borderRadius: '6px', background: 'rgba(129, 140, 248, 0.1)', color: '#818cf8', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Route size={15} />
            </div>
          </div>
          <div>
            <div style={{ fontSize: '28px', fontWeight: '800', color: 'var(--color-text-primary)', fontVariantNumeric: 'tabular-nums' }}>
              {kpis?.km_surveyed ?? 48.6} <span style={{ fontSize: '14px', fontWeight: 600, color: 'var(--color-text-muted)' }}>km</span>
            </div>
            <div style={{ fontSize: '11px', color: 'var(--color-text-secondary)', marginTop: '2px' }}>
              4 survey passes completed today
            </div>
          </div>
        </div>

        {/* Verified Defects */}
        <div className="glass-panel glass-panel-hover" style={{ padding: '18px 20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: '12px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Defects Detected
            </span>
            <div style={{ width: '28px', height: '28px', borderRadius: '6px', background: 'rgba(249, 115, 22, 0.1)', color: 'var(--color-safety-orange)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <AlertOctagon size={15} />
            </div>
          </div>
          <div>
            <div style={{ fontSize: '28px', fontWeight: '800', color: 'var(--color-text-primary)', fontVariantNumeric: 'tabular-nums' }}>
              {kpis?.defects_detected ?? 0}
            </div>
            <div style={{ fontSize: '11px', color: 'var(--color-text-secondary)', marginTop: '2px' }}>
              <b style={{ color: 'var(--color-safety-orange)' }}>{kpis?.defects_corroborated ?? 0} corroborated</b> (2+ buses)
            </div>
          </div>
        </div>

        {/* Bandwidth Saved */}
        <div className="glass-panel glass-panel-hover" style={{ padding: '18px 20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: '12px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Bandwidth Saved
            </span>
            <div style={{ width: '28px', height: '28px', borderRadius: '6px', background: 'rgba(56, 189, 248, 0.1)', color: 'var(--color-accent)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <HardDrive size={15} />
            </div>
          </div>
          <div>
            <div style={{ fontSize: '28px', fontWeight: '800', color: 'var(--color-text-primary)', fontVariantNumeric: 'tabular-nums' }}>
              {kpis?.bandwidth_saved_pct ?? 100}%
            </div>
            <div style={{ fontSize: '11px', color: 'var(--color-text-secondary)', marginTop: '2px' }}>
              1.6 KB JSON vs 2.08 GB video
            </div>
          </div>
        </div>

      </div>

      {/* 3. Main Data Visualization Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.6fr 1fr', gap: '20px' }}>
        
        {/* Main Chart */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h3 style={{ fontSize: '15px', fontWeight: '800', color: 'var(--color-text-primary)', margin: 0 }}>
                Corridor Traffic & Surface Defect Trends
              </h3>
              <p style={{ fontSize: '11px', color: 'var(--color-text-muted)', margin: '2px 0 0 0' }}>
                15-Minute Volume Across Surveyed Arterial Roads
              </p>
            </div>
            <button
              onClick={() => onNavigateTab('traffic')}
              style={{
                background: 'var(--color-surface-elevated)',
                border: '1px solid var(--color-border-default)',
                color: 'var(--color-text-secondary)',
                padding: '5px 12px',
                borderRadius: '6px',
                fontSize: '11px',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              Full Analytics →
            </button>
          </div>

          <div style={{ width: '100%', height: '280px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={timeSeries} margin={{ top: 10, right: 15, left: -15, bottom: 0 }}>
                <defs>
                  <linearGradient id="tonkGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#38bdf8" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="miGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f97316" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="time" stroke="#5E5953" fontSize={11} tickLine={false} />
                <YAxis stroke="#5E5953" fontSize={11} tickLine={false} />
                <Tooltip
                  contentStyle={{ 
                    background: '#191613', 
                    borderColor: '#2A241E', 
                    borderRadius: '8px', 
                    fontSize: '11px',
                    color: '#FEFEFE'
                  }}
                />
                <Area type="monotone" dataKey="tonk_road" name="Tonk Road" stroke="#38bdf8" strokeWidth={2} fillOpacity={1} fill="url(#tonkGrad)" />
                <Area type="monotone" dataKey="mi_road" name="MI Road" stroke="#f97316" strokeWidth={2} fillOpacity={1} fill="url(#miGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Active Bus Fleet Panel */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '15px', fontWeight: '800', color: 'var(--color-text-primary)', margin: 0 }}>
              Live Bus Sensor Units
            </h3>
            <span style={{ fontSize: '11px', color: '#10b981', fontWeight: 700 }}>● 3 Active</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {[
              { id: 'RJ14-01', route: 'Route 9A (MI Road)', speed: '24 km/h', pass: 'Pass 1 Complete', status: 'Active Sensing' },
              { id: 'RJ14-07', route: 'Route 12 (Tonk Road)', speed: '32 km/h', pass: 'Pass 2 Corroborated', status: 'Active Sensing' },
              { id: 'RJ14-12', route: 'Route 3 (Civil Lines)', speed: '19 km/h', pass: 'Re-detection Ready', status: 'Active Sensing' },
            ].map((bus) => (
              <div key={bus.id} style={{
                background: 'var(--color-surface-elevated)',
                border: '1px solid var(--color-border-default)',
                padding: '12px 14px',
                borderRadius: 'var(--radius-md)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <div style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '8px',
                    background: 'var(--color-surface-subtle)',
                    border: '1px solid var(--color-border-default)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--color-accent)'
                  }}>
                    <Bus size={16} />
                  </div>
                  <div>
                    <div style={{ fontSize: '13px', fontWeight: '700', color: 'var(--color-text-primary)' }}>
                      Bus {bus.id}
                    </div>
                    <div style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>
                      {bus.route} · {bus.speed}
                    </div>
                  </div>
                </div>

                <span style={{
                  fontSize: '10px',
                  fontWeight: '700',
                  color: '#10b981',
                  background: 'rgba(16, 185, 129, 0.1)',
                  border: '1px solid rgba(16, 185, 129, 0.25)',
                  padding: '3px 8px',
                  borderRadius: '4px',
                }}>
                  {bus.pass}
                </span>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* 4. Secondary Row: Recent Work Orders & DPDP Compliance Summary */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        
        {/* Top Work Orders */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '15px', fontWeight: '800', color: 'var(--color-text-primary)', margin: 0 }}>
              Top Priority Work Orders
            </h3>
            <button
              onClick={() => onNavigateTab('work_orders')}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--color-accent)',
                fontSize: '11px',
                fontWeight: 700,
                cursor: 'pointer'
              }}
            >
              View Queue ({workOrders.length}) →
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {workOrders.slice(0, 3).map((wo) => (
              <div key={wo.work_order_id} style={{
                background: 'var(--color-surface-elevated)',
                border: '1px solid var(--color-border-default)',
                padding: '12px 14px',
                borderRadius: 'var(--radius-md)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <div style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '6px',
                    background: 'var(--color-surface-subtle)',
                    border: '1px solid var(--color-border-default)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '13px',
                    fontWeight: '800',
                    color: 'var(--color-accent)'
                  }}>
                    {wo.priority_score}
                  </div>
                  <div>
                    <div style={{ fontSize: '12.5px', fontWeight: '700', color: 'var(--color-text-primary)' }}>
                      {wo.title}
                    </div>
                    <div style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>
                      {wo.road_segment}
                    </div>
                  </div>
                </div>

                <span style={{
                  fontSize: '9px',
                  fontWeight: '700',
                  color: 'var(--color-safety-orange)',
                  background: 'rgba(249, 115, 22, 0.1)',
                  padding: '2px 6px',
                  borderRadius: '4px',
                  textTransform: 'uppercase'
                }}>
                  {wo.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* DPDP Compliance Card */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: '14px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
              <ShieldCheck size={18} style={{ color: '#10b981' }} />
              <h3 style={{ fontSize: '15px', fontWeight: '800', color: 'var(--color-text-primary)', margin: 0 }}>
                DPDP Act 2023 Privacy Safeguards
              </h3>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', lineHeight: 1.5, margin: 0 }}>
              All edge cameras execute Gaussian face and license plate de-identification in volatile RAM. 
              Zero facial recognition, zero ANPR, and compact JSON telemetry only.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              onClick={() => onNavigateTab('portal')}
              style={{
                background: 'var(--color-surface-elevated)',
                border: '1px solid var(--color-border-default)',
                color: 'var(--color-text-primary)',
                padding: '8px 14px',
                borderRadius: 'var(--radius-md)',
                fontSize: '11px',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              Read DPDP Charter →
            </button>
          </div>
        </div>

      </div>

    </div>
  );
}
