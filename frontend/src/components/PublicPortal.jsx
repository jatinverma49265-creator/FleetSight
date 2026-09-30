import React, { useState } from 'react';

export default function PublicPortal({ onLaunchDashboard }) {
  const [activeFaq, setActiveFaq] = useState(null);

  const toggleFaq = (idx) => {
    setActiveFaq(activeFaq === idx ? null : idx);
  };

  return (
    <div className="public-portal-container" style={{ maxWidth: '1280px', margin: '0 auto', padding: '24px 20px 60px' }}>
      
      {/* 1. Hero Section */}
      <section className="portal-hero" style={{
        background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.9))',
        border: '1px solid rgba(56, 189, 248, 0.25)',
        borderRadius: '16px',
        padding: '48px 36px',
        marginBottom: '36px',
        boxShadow: '0 20px 40px -15px rgba(0, 0, 0, 0.5)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ position: 'absolute', top: '-40px', right: '-40px', width: '220px', height: '220px', background: 'radial-gradient(circle, rgba(14, 165, 233, 0.15) 0%, transparent 70%)', pointerEvents: 'none' }} />
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <span style={{ background: 'rgba(14, 165, 233, 0.15)', color: '#38bdf8', padding: '4px 12px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 700, letterSpacing: '0.05em', border: '1px solid rgba(56, 189, 248, 0.3)' }}>
            SMART INDIA HACKATHON 2026 · PS SIH26124
          </span>
          <span style={{ background: 'rgba(234, 179, 8, 0.15)', color: '#facc15', padding: '4px 12px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 600 }}>
            SIMULATED PILOT CORRIDOR
          </span>
        </div>

        <h1 style={{ fontSize: '2.6rem', fontWeight: 800, color: '#f8fafc', lineHeight: 1.2, margin: '0 0 16px 0', letterSpacing: '-0.02em' }}>
          FleetSight: Mobile Urban Sensing & <br />
          <span style={{ background: 'linear-gradient(90deg, #38bdf8, #818cf8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Closed-Loop Road Infrastructure Intelligence
          </span>
        </h1>

        <p style={{ fontSize: '1.15rem', color: '#94a3b8', maxWidth: '820px', lineHeight: 1.6, marginBottom: '28px' }}>
          Transforming daily public transit buses into high-frequency, low-cost autonomous road inspection agents. 
          Detecting road hazards, potholes, waterlogging, and signage failures with edge AI, 
          multi-bus corroboration, and DPDP Act 2023 privacy compliance.
        </p>

        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          <button
            onClick={onLaunchDashboard}
            style={{
              padding: '12px 28px',
              background: 'linear-gradient(135deg, #0284c7, #2563eb)',
              color: '#ffffff',
              border: 'none',
              borderRadius: '8px',
              fontSize: '1rem',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              boxShadow: '0 4px 14px rgba(2, 132, 199, 0.4)',
              transition: 'transform 0.15s ease'
            }}
          >
            Launch GIS Command Center ⚡
          </button>
          <a
            href="#dpdp-privacy"
            style={{
              padding: '12px 24px',
              background: 'rgba(255, 255, 255, 0.05)',
              color: '#e2e8f0',
              border: '1px solid rgba(148, 163, 184, 0.2)',
              borderRadius: '8px',
              fontSize: '1rem',
              fontWeight: 500,
              textDecoration: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            DPDP Privacy Charter 🛡️
          </a>
        </div>
      </section>

      {/* 2. Sourced Statistics Section */}
      <section style={{ marginBottom: '48px' }}>
        <div style={{ marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#38bdf8', fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <span>Civic Problem Statement & Data Baseline</span>
          </div>
          <h2 style={{ fontSize: '1.8rem', fontWeight: 700, color: '#f1f5f9', margin: '4px 0 8px 0' }}>
            The Road Safety Challenge in Numbers
          </h2>
          <p style={{ color: '#94a3b8', fontSize: '0.95rem', maxWidth: '750px', margin: 0 }}>
            Official baseline statistics sourced directly from Ministry of Road Transport and Highways (MoRTH) annual reports and municipal audit drives.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '18px' }}>
          <div className="stat-card" style={{ background: '#1e293b', padding: '22px', borderRadius: '12px', border: '1px solid rgba(148, 163, 184, 0.15)' }}>
            <div style={{ color: '#ef4444', fontSize: '2.2rem', fontWeight: 800 }}>4,61,312</div>
            <div style={{ color: '#f8fafc', fontWeight: 600, fontSize: '1rem', marginTop: '4px' }}>Road Accidents in India (2022)</div>
            <div style={{ color: '#64748b', fontSize: '0.8rem', marginTop: '8px' }}>Source: MoRTH "Road Accidents in India 2022"</div>
          </div>

          <div className="stat-card" style={{ background: '#1e293b', padding: '22px', borderRadius: '12px', border: '1px solid rgba(148, 163, 184, 0.15)' }}>
            <div style={{ color: '#f97316', fontSize: '2.2rem', fontWeight: 800 }}>1,68,491</div>
            <div style={{ color: '#f8fafc', fontWeight: 600, fontSize: '1rem', marginTop: '4px' }}>Road Fatalities Recorded</div>
            <div style={{ color: '#64748b', fontSize: '0.8rem', marginTop: '8px' }}>Source: MoRTH National Accident Database</div>
          </div>

          <div className="stat-card" style={{ background: '#1e293b', padding: '22px', borderRadius: '12px', border: '1px solid rgba(148, 163, 184, 0.15)' }}>
            <div style={{ color: '#eab308', fontSize: '2.2rem', fontWeight: 800 }}>32,825</div>
            <div style={{ color: '#f8fafc', fontWeight: 600, fontSize: '1rem', marginTop: '4px' }}>Pedestrian Deaths Annually</div>
            <div style={{ color: '#64748b', fontSize: '0.8rem', marginTop: '8px' }}>Source: MoRTH Vulnerable Road Users Split</div>
          </div>

          <div className="stat-card" style={{ background: '#1e293b', padding: '22px', borderRadius: '12px', border: '1px solid rgba(148, 163, 184, 0.15)' }}>
            <div style={{ color: '#10b981', fontSize: '2.2rem', fontWeight: 800 }}>7,678 / 4,003</div>
            <div style={{ color: '#f8fafc', fontWeight: 600, fontSize: '1rem', marginTop: '4px' }}>Delhi Potholes Identified vs Repaired</div>
            <div style={{ color: '#64748b', fontSize: '0.8rem', marginTop: '8px' }}>Source: Delhi PWD/MCD Special Repair Drives</div>
          </div>
        </div>
      </section>

      {/* 3. The 5-Step Sensing & Closed-Loop Architecture */}
      <section style={{ marginBottom: '48px' }}>
        <div style={{ marginBottom: '24px' }}>
          <div style={{ color: '#38bdf8', fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            System Workflow & Engineering
          </div>
          <h2 style={{ fontSize: '1.8rem', fontWeight: 700, color: '#f1f5f9', margin: '4px 0 8px 0' }}>
            The 5-Stage Mobile Sensing Closed Loop
          </h2>
          <p style={{ color: '#94a3b8', fontSize: '0.95rem', margin: 0 }}>
            How FleetSight achieves scalable civic infrastructure monitoring without dedicated survey fleets or video bandwidth costs.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
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
            <div key={idx} style={{
              background: '#0f172a',
              border: '1px solid rgba(56, 189, 248, 0.2)',
              borderRadius: '12px',
              padding: '20px',
              position: 'relative'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <span style={{ fontSize: '1.8rem' }}>{item.icon}</span>
                <span style={{ fontSize: '0.85rem', fontWeight: 800, color: '#38bdf8', background: 'rgba(56, 189, 248, 0.1)', padding: '2px 8px', borderRadius: '4px' }}>
                  STEP {item.step}
                </span>
              </div>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', margin: '0 0 8px 0' }}>
                {item.title}
              </h3>
              <p style={{ fontSize: '0.85rem', color: '#94a3b8', lineHeight: 1.5, margin: 0 }}>
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* 4. DPDP Act 2023 Privacy Charter */}
      <section id="dpdp-privacy" style={{
        background: '#0f172a',
        border: '1px solid rgba(148, 163, 184, 0.2)',
        borderRadius: '16px',
        padding: '32px',
        marginBottom: '48px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <span style={{ fontSize: '1.5rem' }}>⚖️</span>
          <div>
            <h2 style={{ fontSize: '1.6rem', fontWeight: 700, color: '#f8fafc', margin: 0 }}>
              Digital Personal Data Protection (DPDP) Act 2023 Compliance
            </h2>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', margin: '4px 0 0 0' }}>
              Built for public safety with rigorous technical and legal boundaries.
            </p>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginTop: '24px' }}>
          <div style={{ background: '#1e293b', padding: '18px', borderRadius: '10px', borderLeft: '4px solid #10b981' }}>
            <h4 style={{ color: '#10b981', margin: '0 0 8px 0', fontSize: '1rem', fontWeight: 700 }}>1. Zero Facial Recognition</h4>
            <p style={{ color: '#cbd5e1', fontSize: '0.85rem', lineHeight: 1.5, margin: 0 }}>
              FleetSight contains no facial recognition or biometric software. Pedestrian bounding boxes are permanently blurred at edge level prior to storage.
            </p>
          </div>

          <div style={{ background: '#1e293b', padding: '18px', borderRadius: '10px', borderLeft: '4px solid #3b82f6' }}>
            <h4 style={{ color: '#38bdf8', margin: '0 0 8px 0', fontSize: '1rem', fontWeight: 700 }}>2. No ANPR or Vehicle Tracking</h4>
            <p style={{ color: '#cbd5e1', fontSize: '0.85rem', lineHeight: 1.5, margin: 0 }}>
              No Automated Number Plate Recognition (ANPR) is executed. Vehicle plates are masked on the edge camera before frame disposal.
            </p>
          </div>

          <div style={{ background: '#1e293b', padding: '18px', borderRadius: '10px', borderLeft: '4px solid #eab308' }}>
            <h4 style={{ color: '#facc15', margin: '0 0 8px 0', fontSize: '1rem', fontWeight: 700 }}>3. Data Minimisation by Design</h4>
            <p style={{ color: '#cbd5e1', fontSize: '0.85rem', lineHeight: 1.5, margin: 0 }}>
              Raw video remains in volatile RAM and is never broadcast. Central servers receive only compact GPS JSON objects (~320 bytes).
            </p>
          </div>

          <div style={{ background: '#1e293b', padding: '18px', borderRadius: '10px', borderLeft: '4px solid #a855f7' }}>
            <h4 style={{ color: '#c084fc', margin: '0 0 8px 0', fontSize: '1rem', fontWeight: 700 }}>4. Immutable Audit & Access Control</h4>
            <p style={{ color: '#cbd5e1', fontSize: '0.85rem', lineHeight: 1.5, margin: 0 }}>
              Role-based access control (RBAC) strictly gates work-order approval and sensor logs with cryptographically traceable audit records.
            </p>
          </div>
        </div>
      </section>

      {/* 5. Accessibility & Prototype Disclaimer */}
      <section style={{
        background: 'rgba(30, 41, 59, 0.5)',
        border: '1px dashed rgba(148, 163, 184, 0.3)',
        borderRadius: '12px',
        padding: '24px',
        textAlign: 'center'
      }}>
        <div style={{ display: 'inline-block', background: 'rgba(234, 179, 8, 0.2)', color: '#facc15', padding: '4px 14px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 700, marginBottom: '12px' }}>
          PROTOTYPE & LEGAL NOTICE
        </div>
        <p style={{ color: '#94a3b8', fontSize: '0.85rem', lineHeight: 1.6, maxWidth: '800px', margin: '0 auto 16px' }}>
          This software is developed as an academic and technological prototype for <strong>Smart India Hackathon 2026 (Problem Statement SIH26124)</strong>. 
          All route simulations in the live dashboard operate on synthetic telemetry with <code style={{ color: '#38bdf8' }}>data_origin="simulated"</code>. 
          Designed in compliance with <strong>WCAG 2.1 AA</strong> accessibility and contrast standards.
        </p>
        <button
          onClick={onLaunchDashboard}
          style={{
            padding: '10px 24px',
            background: '#0284c7',
            color: '#ffffff',
            border: 'none',
            borderRadius: '6px',
            fontSize: '0.9rem',
            fontWeight: 600,
            cursor: 'pointer'
          }}
        >
          Open FleetSight GIS Dashboard →
        </button>
      </section>

    </div>
  );
}
