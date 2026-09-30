import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { Filter } from 'lucide-react';

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

    // Clean light cartographic tiles
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
          <div style="font-size: 12px; line-height: 1.4; color: #0D1B2A;">
            <b style="color: #1B263B; font-size: 13px;">🚌 Bus Sensing Unit: ${bus.id}</b>
            <div style="color: #415A77; margin-top: 4px;">${bus.route}</div>
            <div style="font-size: 11px; margin-top: 4px; color: #1B263B;">Speed: <b>${bus.speed}</b> · Edge AI Active</div>
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
      let markerColor = '#1d4ed8'; // low
      if (issue.severity === 'critical') markerColor = '#b91c1c';
      else if (issue.severity === 'high') markerColor = '#ea580c';
      else if (issue.severity === 'medium') markerColor = '#b45309';

      // Status Badge Symbol
      const isVerified = issue.status === 'verified' || issue.status === 'work_order';
      const symbol = isVerified ? '✓' : '!';

      const iconHtml = `
        <div class="pulsing-marker" style="
          width: ${isSelected ? '36px' : '28px'};
          height: ${isSelected ? '36px' : '28px'};
          background: ${markerColor};
          border: ${isSelected ? '3px solid #0D1B2A' : '2px solid #FFFFFF'};
          color: #FFFFFF;
          font-weight: 800;
          font-size: ${isSelected ? '14px' : '11px'};
          transform: translate(-50%, -50%);
          box-shadow: 0 2px 10px ${markerColor}66;
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
    <div className="animate-fade-in" style={{ position: 'relative', width: '100%', height: 'calc(100vh - 210px)', minHeight: '520px', borderRadius: 'var(--radius-lg)', overflow: 'hidden', border: '1px solid var(--color-border-default)', boxShadow: 'var(--shadow-md)' }}>
      
      {/* Map Element */}
      <div id="gis-leaflet-map" ref={mapContainerRef} style={{ width: '100%', height: '100%' }} />

      {/* Floating Filter Bar */}
      <div style={{
        position: 'absolute',
        top: '16px',
        left: '16px',
        zIndex: 500,
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(16px)',
        border: '1px solid var(--color-border-default)',
        borderRadius: 'var(--radius-md)',
        padding: '6px 10px',
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
        boxShadow: 'var(--shadow-md)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', paddingRight: '8px', borderRight: '1px solid var(--color-border-default)', color: 'var(--c-slate-blue)', fontSize: '11px', fontWeight: '700' }}>
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
              background: activeFilter === f.id ? 'var(--c-deep-navy)' : 'var(--color-surface-subtle)',
              color: activeFilter === f.id ? '#FFFFFF' : 'var(--c-deep-navy)',
              border: 'none',
              padding: '5px 12px',
              borderRadius: '6px',
              fontSize: '11px',
              fontWeight: '700',
              cursor: 'pointer',
              transition: 'all var(--transition-fast)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              boxShadow: activeFilter === f.id ? '0 2px 6px rgba(13, 27, 42, 0.16)' : 'none'
            }}
          >
            <span>{f.label}</span>
            <span style={{
              background: activeFilter === f.id ? 'rgba(255, 255, 255, 0.2)' : 'rgba(65, 90, 119, 0.12)',
              color: activeFilter === f.id ? '#FFFFFF' : 'var(--c-deep-navy)',
              padding: '1px 6px',
              borderRadius: '8px',
              fontSize: '10px',
              fontWeight: 800
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
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(16px)',
        border: '1px solid var(--color-border-default)',
        borderRadius: 'var(--radius-md)',
        padding: '10px 16px',
        fontSize: '11px',
        display: 'flex',
        flexDirection: 'column',
        gap: '6px',
        boxShadow: 'var(--shadow-md)',
      }}>
        <span style={{ fontWeight: '800', color: 'var(--c-rich-navy)', fontSize: '10.5px', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
          Severity Map Legend
        </span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <span style={{ width: '9px', height: '9px', borderRadius: '50%', background: '#b91c1c', display: 'inline-block' }}></span>
            <span style={{ color: 'var(--c-deep-navy)', fontWeight: 600 }}>Critical</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <span style={{ width: '9px', height: '9px', borderRadius: '50%', background: '#ea580c', display: 'inline-block' }}></span>
            <span style={{ color: 'var(--c-deep-navy)', fontWeight: 600 }}>High</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <span style={{ width: '9px', height: '9px', borderRadius: '50%', background: '#b45309', display: 'inline-block' }}></span>
            <span style={{ color: 'var(--c-deep-navy)', fontWeight: 600 }}>Medium</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <span style={{ width: '9px', height: '9px', borderRadius: '50%', background: '#1d4ed8', display: 'inline-block' }}></span>
            <span style={{ color: 'var(--c-deep-navy)', fontWeight: 600 }}>Low</span>
          </div>
        </div>
      </div>

    </div>
  );
}
