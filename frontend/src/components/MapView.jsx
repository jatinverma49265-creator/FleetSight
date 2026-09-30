import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import { Filter, Layers, Navigation, Info, Eye, CheckCircle2, AlertCircle } from 'lucide-react';

export default function MapView({ issues, onSelectIssue, selectedIssueId, activeFilter, setActiveFilter }) {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersGroupRef = useRef(null);
  const busesGroupRef = useRef(null);

  // Jaipur Center
  const JAIPUR_CENTER = [26.8950, 75.8070];

  // Bus locations on active corridors
  const BUS_FLEET = [
    { id: 'RJ14-01', lat: 26.9180, lng: 75.8150, route: 'Route 9A (MI Road -> Tonk Road)', speed: '24 km/h' },
    { id: 'RJ14-07', lat: 26.8850, lng: 75.8110, route: 'Route 12 (JLN Marg Express)', speed: '32 km/h' },
    { id: 'RJ14-12', lat: 26.8670, lng: 75.7980, route: 'Route 3 (Civil Lines Loop)', speed: '19 km/h' },
  ];

  // Initialize Map
  useEffect(() => {
    if (!mapContainerRef.current) return;
    if (mapInstanceRef.current) return;

    const map = L.map(mapContainerRef.current, {
      center: JAIPUR_CENTER,
      zoom: 13,
      zoomControl: false,
    });

    L.control.zoom({ position: 'bottomright' }).addTo(map);

    // OpenStreetMap standard tiles with CSS dark inversion filter
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(map);

    markersGroupRef.current = L.layerGroup().addTo(map);
    busesGroupRef.current = L.layerGroup().addTo(map);

    mapInstanceRef.current = map;

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  // Update Markers when issues change
  useEffect(() => {
    if (!mapInstanceRef.current || !markersGroupRef.current || !busesGroupRef.current) return;

    markersGroupRef.current.clearLayers();
    busesGroupRef.current.clearLayers();

    // 1. Render Public Bus Markers
    BUS_FLEET.forEach((bus) => {
      const busHtml = `
        <div class="bus-marker" style="transform: translate(-50%, -50%);">
          <span style="font-size: 13px;">🚌</span>
          <span>${bus.id}</span>
        </div>
      `;
      const busIcon = L.divIcon({
        html: busHtml,
        className: 'custom-bus-icon',
        iconSize: [80, 24],
      });

      const marker = L.marker([bus.lat, bus.lng], { icon: busIcon })
        .bindPopup(`
          <div style="font-size: 12px; line-height: 1.4;">
            <b style="color: #00d2b4;">🚌 Bus Sensing Unit: ${bus.id}</b>
            <div style="color: #889ba8; margin-top: 4px;">${bus.route}</div>
            <div style="font-size: 11px; margin-top: 4px;">Speed: <b>${bus.speed}</b> · Edge AI Active</div>
          </div>
        `);
      busesGroupRef.current.addLayer(marker);
    });

    // 2. Render Issue Markers
    const filteredIssues = issues.filter((issue) => {
      if (activeFilter === 'all') return true;
      return issue.status === activeFilter;
    });

    filteredIssues.forEach((issue) => {
      const isSelected = selectedIssueId === issue.issue_id;
      
      // Color by severity
      let markerColor = '#3b82f6'; // low
      if (issue.severity === 'critical') markerColor = '#ef4444';
      else if (issue.severity === 'high') markerColor = '#ff7a00';
      else if (issue.severity === 'medium') markerColor = '#eab308';

      // Status Badge Symbol
      const isVerified = issue.status === 'verified' || issue.status === 'work_order';
      const symbol = isVerified ? '✓' : '!';

      const iconHtml = `
        <div class="pulsing-marker" style="
          width: ${isSelected ? '36px' : '28px'};
          height: ${isSelected ? '36px' : '28px'};
          background: ${markerColor};
          border: ${isSelected ? '3px solid #fff' : '2px solid rgba(255,255,255,0.85)'};
          color: #fff;
          font-weight: 800;
          font-size: ${isSelected ? '14px' : '11px'};
          transform: translate(-50%, -50%);
          box-shadow: 0 0 ${isSelected ? '20px' : '10px'} ${markerColor}88;
        ">
          ${symbol}
        </div>
      `;

      const customIcon = L.divIcon({
        html: iconHtml,
        className: 'custom-issue-icon',
        iconSize: [32, 32],
      });

      const marker = L.marker([issue.latitude, issue.longitude], { icon: customIcon });

      marker.on('click', () => {
        onSelectIssue(issue.issue_id);
      });

      markersGroupRef.current.addLayer(marker);
    });
  }, [issues, activeFilter, selectedIssueId]);

  return (
    <div style={{ position: 'relative', width: '100%', height: 'calc(100vh - 200px)', minHeight: '520px', borderRadius: '12px', overflow: 'hidden', border: '1px solid var(--border-subtle)' }}>
      
      {/* Map Element */}
      <div id="gis-leaflet-map" ref={mapContainerRef} style={{ width: '100%', height: '100%' }} />

      {/* Floating Filter Bar */}
      <div style={{
        position: 'absolute',
        top: '16px',
        left: '16px',
        zIndex: 500,
        background: 'rgba(14, 25, 35, 0.92)',
        backdropFilter: 'blur(12px)',
        border: '1px solid var(--border-subtle)',
        borderRadius: '10px',
        padding: '6px 10px',
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
        boxShadow: '0 8px 30px rgba(0,0,0,0.5)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', paddingRight: '8px', borderRight: '1px solid var(--border-subtle)', color: 'var(--text-dim)', fontSize: '11px', fontWeight: '700' }}>
          <Filter size={13} />
          <span>STATUS:</span>
        </div>

        {[
          { id: 'all', label: 'All Issues', count: issues.length },
          { id: 'candidate', label: 'Candidates', count: issues.filter(i => i.status === 'candidate').length },
          { id: 'verified', label: 'Verified (2+ Buses)', count: issues.filter(i => i.status === 'verified').length },
          { id: 'work_order', label: 'Work Orders', count: issues.filter(i => i.status === 'work_order').length },
          { id: 'repaired', label: 'Repaired', count: issues.filter(i => i.status === 'repaired').length },
        ].map((f) => (
          <button
            key={f.id}
            id={`filter-btn-${f.id}`}
            onClick={() => setActiveFilter(f.id)}
            style={{
              background: activeFilter === f.id ? 'var(--brand-teal)' : 'rgba(255,255,255,0.05)',
              color: activeFilter === f.id ? '#070d13' : 'var(--text-muted)',
              border: 'none',
              padding: '4px 10px',
              borderRadius: '6px',
              fontSize: '11px',
              fontWeight: '700',
              cursor: 'pointer',
              transition: 'all 0.15s ease',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
            }}
          >
            <span>{f.label}</span>
            <span style={{
              background: activeFilter === f.id ? 'rgba(0,0,0,0.25)' : 'rgba(255,255,255,0.1)',
              padding: '1px 5px',
              borderRadius: '10px',
              fontSize: '9px',
            }}>
              {f.count}
            </span>
          </button>
        ))}
      </div>

      {/* Floating Legend */}
      <div style={{
        position: 'absolute',
        bottom: '16px',
        left: '16px',
        zIndex: 500,
        background: 'rgba(14, 25, 35, 0.92)',
        backdropFilter: 'blur(12px)',
        border: '1px solid var(--border-subtle)',
        borderRadius: '10px',
        padding: '10px 14px',
        fontSize: '11px',
        display: 'flex',
        flexDirection: 'column',
        gap: '6px',
        boxShadow: '0 8px 30px rgba(0,0,0,0.5)',
      }}>
        <span style={{ fontWeight: '700', color: '#fff', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
          Severity Map Legend
        </span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ef4444', display: 'inline-block' }}></span>
            <span>Critical</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff7a00', display: 'inline-block' }}></span>
            <span>High</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#eab308', display: 'inline-block' }}></span>
            <span>Medium</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#3b82f6', display: 'inline-block' }}></span>
            <span>Low</span>
          </div>
        </div>
      </div>

    </div>
  );
}
