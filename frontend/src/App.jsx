import React, { useEffect, useState, useCallback } from 'react';
import Navbar from './components/Navbar';
import KPIRow from './components/KPIRow';
import DemoControlPanel from './components/DemoControlPanel';
import BytesComparisonModal from './components/BytesComparisonModal';
import MapView from './components/MapView';
import IssueDetailDrawer from './components/IssueDetailDrawer';
import WorkOrdersView from './components/WorkOrdersView';
import TrafficView from './components/TrafficView';
import AuditView from './components/AuditView';
import RBACDenialModal from './components/RBACDenialModal';
import { fetchKPIs, fetchIssues, fetchWorkOrders, fetchTraffic } from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState('map');
  const [currentRole, setCurrentRole] = useState('engineer');
  const [kpis, setKpis] = useState(null);
  const [issues, setIssues] = useState([]);
  const [workOrders, setWorkOrders] = useState([]);
  const [trafficData, setTrafficData] = useState(null);
  const [selectedIssueId, setSelectedIssueId] = useState(null);
  const [activeFilter, setActiveFilter] = useState('all');
  const [lastUpdated, setLastUpdated] = useState(null);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [denialModal, setDenialModal] = useState({ open: false, message: '' });
  const [bytesModalOpen, setBytesModalOpen] = useState(false);

  // Load state from backend
  const loadData = useCallback(async (showIndicator = false) => {
    if (showIndicator) setIsRefreshing(true);
    try {
      const [kpiRes, issueRes, woRes, trafRes] = await Promise.all([
        fetchKPIs().catch(() => null),
        fetchIssues().catch(() => []),
        fetchWorkOrders().catch(() => []),
        fetchTraffic().catch(() => null),
      ]);

      if (kpiRes) setKpis(kpiRes);
      if (issueRes) {
        setIssues(issueRes);
        if (!selectedIssueId && issueRes.length > 0) {
          setSelectedIssueId(issueRes[0].issue_id);
        }
      }
      if (woRes) setWorkOrders(woRes);
      if (trafRes) setTrafficData(trafRes);
      setLastUpdated(new Date());
    } catch (err) {
      console.error('Data sync failed:', err);
    } finally {
      if (showIndicator) setIsRefreshing(false);
    }
  }, [selectedIssueId]);

  // Initial load
  useEffect(() => {
    loadData(true);
  }, []);

  // Polling every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      loadData(false);
    }, 5000);
    return () => clearInterval(interval);
  }, [loadData]);

  const selectedIssue = issues.find((i) => i.issue_id === selectedIssueId) || issues[0] || null;

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentRole={currentRole}
        setCurrentRole={setCurrentRole}
        lastUpdated={lastUpdated}
        onRefresh={() => loadData(true)}
        isRefreshing={isRefreshing}
      />

      {/* KPI Overview Bar */}
      <KPIRow kpis={kpis} />

      {/* Demo Control Bar for Loop 7 */}
      <DemoControlPanel
        onRefresh={() => loadData(true)}
        onOpenBytesModal={() => setBytesModalOpen(true)}
      />

      {/* Main Content Body */}
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        
        {/* Map Tab */}
        {activeTab === 'map' && (
          <div style={{
            display: 'flex',
            gap: '16px',
            margin: '20px 24px',
            position: 'relative',
          }}>
            <div style={{ flex: 1 }}>
              <MapView
                issues={issues}
                onSelectIssue={(id) => setSelectedIssueId(id)}
                selectedIssueId={selectedIssueId}
                activeFilter={activeFilter}
                setActiveFilter={setActiveFilter}
              />
            </div>

            {selectedIssue && (
              <IssueDetailDrawer
                issue={selectedIssue}
                onClose={() => setSelectedIssueId(null)}
              />
            )}
          </div>
        )}

        {/* Work Orders Tab */}
        {activeTab === 'work_orders' && (
          <WorkOrdersView
            workOrders={workOrders}
            currentRole={currentRole}
            onRefresh={() => loadData(true)}
            onTriggerDenialModal={(msg) => setDenialModal({ open: true, message: msg })}
          />
        )}

        {/* Traffic Heatmap Tab */}
        {activeTab === 'traffic' && (
          <TrafficView trafficData={trafficData} />
        )}

        {/* Audit Trail Tab */}
        {activeTab === 'audit' && (
          <AuditView currentRole={currentRole} />
        )}

      </main>

      {/* RBAC Denial Modal */}
      <RBACDenialModal
        isOpen={denialModal.open}
        message={denialModal.message}
        onClose={() => setDenialModal({ open: false, message: '' })}
        currentRole={currentRole}
      />

      {/* Bytes vs 720p Video Analysis Modal */}
      <BytesComparisonModal
        isOpen={bytesModalOpen}
        onClose={() => setBytesModalOpen(false)}
      />

    </div>
  );
}
