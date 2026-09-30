import React from 'react';

export default function PublicPortal({ onLaunchDashboard }) {
  return (
    <div className="public-portal-container animate-fade-in" style={{ maxWidth: '1280px', margin: '0 auto', padding: '24px 28px 60px' }}>
      
      {/* 1. Hero Section */}
      <section className="portal-hero" style={{
        background: 'linear-gradient(135deg, var(--c-deep-navy) 0%, var(--c-rich-navy) 100%)',
        border: '1px solid var(--c-slate-blue)',
        borderRadius: 'var(--radius-xl)',
        padding: '52px 44px',
        marginBottom: '40px',
        boxShadow: 'var(--shadow-lg)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ position: 'absolute', top: '-40px', right: '-40px', width: '280px', height: '280px', background: 'radial-gradient(circle, rgba(119, 141, 169, 0.22) 0%, transparent 70%)', pointerEvents: 'none' }} />
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '18px' }}>
          <span style={{ background: 'rgba(224, 225, 221, 0.14)', color: '#E0E1DD', padding: '5px 14px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 700, letterSpacing: '0.05em', border: '1px solid rgba(224, 225, 221, 0.25)' }}>
            SMART URBAN SENSING · CLOSED-LOOP ROAD AI
          </span>
          <span style={{ background: 'rgba(234, 88, 12, 0.18)', color: '#fdba74', padding: '5px 14px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 700 }}>
            SIMULATED PILOT CORRIDOR
          </span>
        </div>

        <h1 style={{ fontSize: '2.85rem', fontWeight: 800, color: '#FFFFFF', lineHeight: 1.2, margin: '0 0 16px 0', letterSpacing: '-0.02em' }}>
          FleetSight: Mobile Urban Sensing & <br />
          <span style={{ background: 'linear-gradient(90deg, #E0E1DD, #778DA9)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Closed-Loop Road Infrastructure Intelligence
          </span>
        </h1>

        <p style={{ fontSize: '1.12rem', color: '#D4CFCA', maxWidth: '840px', lineHeight: 1.6, marginBottom: '32px', fontWeight: 400 }}>
          Transforming regular municipal transit buses into high-frequency, low-cost autonomous road inspection agents. 
          Detecting road hazards, potholes, waterlogging, and damaged signage with edge AI, 
          multi-bus corroboration, and DPDP Act 2023 privacy compliance.
        </p>

        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          <button
            id="btn-launch-command-center"
            aria-label="Launch GIS Command Center"
            onClick={onLaunchDashboard}
            style={{
              padding: '13px 32px',
              background: 'var(--c-light-bg)',
              color: 'var(--c-rich-navy)',
              border: 'none',
              borderRadius: 'var(--radius-md)',
              fontSize: '1rem',
              fontWeight: 800,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              boxShadow: '0 4px 16px rgba(0, 0, 0, 0.25)',
              transition: 'all var(--transition-fast)'
            }}
          >
            Launch GIS Command Center ⚡
          </button>
          <a
            href="#dpdp-privacy"
            style={{
              padding: '13px 26px',
              background: 'rgba(255, 255, 255, 0.1)',
              color: '#FFFFFF',
              border: '1px solid rgba(224, 225, 221, 0.3)',
              borderRadius: 'var(--radius-md)',
              fontSize: '1rem',
              fontWeight: 600,
              textDecoration: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'all var(--transition-fast)'
            }}
          >
            DPDP Privacy Charter 🛡️
          </a>
        </div>
      </section>

      {/* 2. Sourced Statistics Section */}
      <section style={{ marginBottom: '52px' }}>
        <div style={{ marginBottom: '22px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--c-slate-blue)', fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            <span>Civic Problem Statement & Data Baseline</span>
          </div>
          <h2 style={{ fontSize: '1.9rem', fontWeight: 800, color: 'var(--c-rich-navy)', margin: '4px 0 8px 0' }}>
            The Road Safety Challenge in Numbers
          </h2>
          <p style={{ color: 'var(--c-slate-blue)', fontSize: '0.95rem', maxWidth: '780px', margin: 0, fontWeight: 500 }}>
            Official baseline statistics sourced directly from Ministry of Road Transport and Highways (MoRTH 2022) annual reports and municipal audit drives.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '18px' }}>
          <div className="glass-panel glass-panel-hover" style={{ padding: '24px' }}>
            <div style={{ color: '#b91c1c', fontSize: '2.2rem', fontWeight: 800, fontVariantNumeric: 'tabular-nums' }}>4,61,312</div>
            <div style={{ color: 'var(--c-rich-navy)', fontWeight: 700, fontSize: '1rem', marginTop: '6px' }}>Road Accidents in India (2022)</div>
            <div style={{ color: 'var(--c-slate-blue)', fontSize: '0.8rem', marginTop: '8px' }}>Source: MoRTH "Road Accidents in India 2022"</div>
          </div>

          <div className="glass-panel glass-panel-hover" style={{ padding: '24px' }}>
            <div style={{ color: 'var(--color-safety-orange)', fontSize: '2.2rem', fontWeight: 800, fontVariantNumeric: 'tabular-nums' }}>1,68,491</div>
            <div style={{ color: 'var(--c-rich-navy)', fontWeight: 700, fontSize: '1rem', marginTop: '6px' }}>Road Fatalities Recorded</div>
            <div style={{ color: 'var(--c-slate-blue)', fontSize: '0.8rem', marginTop: '8px' }}>Source: MoRTH National Accident Database</div>
          </div>

          <div className="glass-panel glass-panel-hover" style={{ padding: '24px' }}>
            <div style={{ color: '#b45309', fontSize: '2.2rem', fontWeight: 800, fontVariantNumeric: 'tabular-nums' }}>32,825</div>
            <div style={{ color: 'var(--c-rich-navy)', fontWeight: 700, fontSize: '1rem', marginTop: '6px' }}>Pedestrian Deaths Annually</div>
            <div style={{ color: 'var(--c-slate-blue)', fontSize: '0.8rem', marginTop: '8px' }}>Source: MoRTH Vulnerable Road Users Split</div>
          </div>

          <div className="glass-panel glass-panel-hover" style={{ padding: '24px' }}>
            <div style={{ color: '#15803d', fontSize: '2.2rem', fontWeight: 800, fontVariantNumeric: 'tabular-nums' }}>7,678 / 4,003</div>
            <div style={{ color: 'var(--c-rich-navy)', fontWeight: 700, fontSize: '1rem', marginTop: '6px' }}>Delhi Potholes Identified vs Repaired</div>
            <div style={{ color: 'var(--c-slate-blue)', fontSize: '0.8rem', marginTop: '8px' }}>Source: Delhi PWD/MCD Special Repair Drives</div>
          </div>
        </div>
      </section>

      {/* 3. The 5-Step Sensing & Closed-Loop Architecture */}
      <section style={{ marginBottom: '52px' }}>
        <div style={{ marginBottom: '24px' }}>
          <div style={{ color: 'var(--c-slate-blue)', fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            System Workflow & Engineering
          </div>
          <h2 style={{ fontSize: '1.9rem', fontWeight: 800, color: 'var(--c-rich-navy)', margin: '4px 0 8px 0' }}>
            The 5-Stage Mobile Sensing Closed Loop
          </h2>
          <p style={{ color: 'var(--c-slate-blue)', fontSize: '0.95rem', margin: 0, fontWeight: 500 }}>
            How FleetSight achieves scalable civic infrastructure monitoring without dedicated survey fleets or video bandwidth costs.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '18px' }}>
          {[
            {
              step: '01',
              title: 'Low-Cost Edge Sensing',
              desc: 'Dashcams on existing municipal buses process video in volatile RAM. No heavy cloud streaming.',
              icon: '🚌'
            },
            {
              step: '02',
              title: 'Instant Edge Privacy Blur',
              desc: 'Automatic face and license plate masking before any bounding box or telemetry is cached.',
              icon: '🛡️'
            },
            {
              step: '03',
              title: 'Compact GPS Telemetry',
              desc: 'Transmits ~320 byte JSON events over 4G/5G, saving 99.99% network bandwidth versus raw video.',
              icon: '📡'
            },
            {
              step: '04',
              title: '2+ Bus Corroboration',
              desc: 'Spatial clustering (<=35m) requires independent confirmation from multiple buses, filtering false positives.',
              icon: '📍'
            },
            {
              step: '05',
              title: 'Closed-Loop Verification',
              desc: 'Subsequent bus passes automatically detect repairs to close work orders or escalate persistent defects.',
              icon: '🔄'
            }
          ].map((item, idx) => (
            <div key={idx} className="glass-panel glass-panel-hover" style={{
              padding: '24px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              gap: '12px',
            }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
                  <span style={{ fontSize: '1.8rem' }}>{item.icon}</span>
                  <span style={{ fontSize: '0.8rem', fontWeight: 800, color: 'var(--c-deep-navy)', background: 'var(--color-surface-subtle)', border: '1px solid var(--color-border-subtle)', padding: '3px 8px', borderRadius: '4px' }}>
                    STEP {item.step}
                  </span>
                </div>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--c-rich-navy)', margin: '0 0 8px 0' }}>
                  {item.title}
                </h3>
                <p style={{ fontSize: '0.85rem', color: 'var(--c-slate-blue)', lineHeight: 1.55, margin: 0, fontWeight: 500 }}>
                  {item.desc}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 4. DPDP Act 2023 Privacy Charter */}
      <section id="dpdp-privacy" className="glass-panel" style={{
        padding: '36px',
        marginBottom: '52px',
        borderRadius: 'var(--radius-xl)',
        background: '#FFFFFF'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
          <span style={{ fontSize: '1.6rem' }}>⚖️</span>
          <div>
            <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--c-rich-navy)', margin: 0 }}>
              Digital Personal Data Protection (DPDP) Act 2023 Compliance
            </h2>
            <p style={{ color: 'var(--c-slate-blue)', fontSize: '0.9rem', margin: '4px 0 0 0', fontWeight: 500 }}>
              Built for public safety with rigorous technical and legal privacy boundaries.
            </p>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginTop: '24px' }}>
          <div style={{ background: 'var(--color-surface-subtle)', padding: '20px', borderRadius: 'var(--radius-md)', borderLeft: '4px solid #15803d', border: '1px solid var(--color-border-default)' }}>
            <h4 style={{ color: '#15803d', margin: '0 0 8px 0', fontSize: '1rem', fontWeight: 800 }}>1. Zero Facial Recognition</h4>
            <p style={{ color: 'var(--c-slate-blue)', fontSize: '0.85rem', lineHeight: 1.5, margin: 0, fontWeight: 500 }}>
              FleetSight contains no facial recognition or biometric software. Pedestrian bounding boxes are permanently blurred at edge level prior to storage.
            </p>
          </div>

          <div style={{ background: 'var(--color-surface-subtle)', padding: '20px', borderRadius: 'var(--radius-md)', borderLeft: '4px solid var(--c-deep-navy)', border: '1px solid var(--color-border-default)' }}>
            <h4 style={{ color: 'var(--c-deep-navy)', margin: '0 0 8px 0', fontSize: '1rem', fontWeight: 800 }}>2. No ANPR or Vehicle Tracking</h4>
            <p style={{ color: 'var(--c-slate-blue)', fontSize: '0.85rem', lineHeight: 1.5, margin: 0, fontWeight: 500 }}>
              No Automated Number Plate Recognition (ANPR) is executed. Vehicle plates are masked on the edge camera before frame disposal.
            </p>
          </div>

          <div style={{ background: 'var(--color-surface-subtle)', padding: '20px', borderRadius: 'var(--radius-md)', borderLeft: '4px solid #b45309', border: '1px solid var(--color-border-default)' }}>
            <h4 style={{ color: '#b45309', margin: '0 0 8px 0', fontSize: '1rem', fontWeight: 800 }}>3. Data Minimisation by Design</h4>
            <p style={{ color: 'var(--c-slate-blue)', fontSize: '0.85rem', lineHeight: 1.5, margin: 0, fontWeight: 500 }}>
              Raw video remains in volatile RAM and is never broadcast. Central servers receive only compact GPS JSON objects (~320 bytes).
            </p>
          </div>

          <div style={{ background: 'var(--color-surface-subtle)', padding: '20px', borderRadius: 'var(--radius-md)', borderLeft: '4px solid var(--c-slate-blue)', border: '1px solid var(--color-border-default)' }}>
            <h4 style={{ color: 'var(--c-slate-blue)', margin: '0 0 8px 0', fontSize: '1rem', fontWeight: 800 }}>4. Immutable Audit & Access Control</h4>
            <p style={{ color: 'var(--c-slate-blue)', fontSize: '0.85rem', lineHeight: 1.5, margin: 0, fontWeight: 500 }}>
              Role-based access control (RBAC) strictly gates work-order approval and sensor logs with cryptographically traceable audit records.
            </p>
          </div>
        </div>
      </section>

      {/* 5. Accessibility & Prototype Disclaimer */}
      <section style={{
        background: '#FFFFFF',
        border: '1px dashed var(--c-soft-steel)',
        borderRadius: 'var(--radius-lg)',
        padding: '32px',
        textAlign: 'center',
        boxShadow: 'var(--shadow-sm)'
      }}>
        <div style={{ display: 'inline-block', background: 'rgba(180, 83, 9, 0.1)', color: '#b45309', padding: '4px 14px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 700, marginBottom: '12px' }}>
          PROTOTYPE & LEGAL NOTICE
        </div>
        <p style={{ color: 'var(--c-slate-blue)', fontSize: '0.85rem', lineHeight: 1.6, maxWidth: '800px', margin: '0 auto 16px', fontWeight: 500 }}>
          This software is developed as an advanced municipal infrastructure sensing and closed-loop inspection platform. 
          All route simulations in the live dashboard operate on synthetic telemetry with <code style={{ color: 'var(--c-deep-navy)', fontWeight: 700 }}>data_origin="simulated"</code>. 
          Designed in compliance with <strong>WCAG 2.1 AA</strong> accessibility and contrast standards.
        </p>
        <button
          onClick={onLaunchDashboard}
          style={{
            padding: '11px 26px',
            background: 'var(--c-deep-navy)',
            color: '#FFFFFF',
            border: 'none',
            borderRadius: 'var(--radius-sm)',
            fontSize: '0.9rem',
            fontWeight: 700,
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(13, 27, 42, 0.2)',
            transition: 'all var(--transition-fast)'
          }}
        >
          Open FleetSight GIS Dashboard →
        </button>
      </section>

    </div>
  );
}
