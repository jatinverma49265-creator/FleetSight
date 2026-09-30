import React, { useEffect, useState, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import DashboardOverview from './components/DashboardOverview';
import DemoControlPanel from './components/DemoControlPanel';
import BytesComparisonModal from './components/BytesComparisonModal';
import MapView from './components/MapView';
import IssueDetailDrawer from './components/IssueDetailDrawer';
import WorkOrdersView from './components/WorkOrdersView';
import TrafficView from './components/TrafficView';
import AuditView from './components/AuditView';
import RBACDenialModal from './components/RBACDenialModal';
import PublicPortal from './components/PublicPortal';
import { fetchKPIs, fetchIssues, fetchWorkOrders, fetchTraffic } from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState('portal');
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
    <div className="app-layout">
      
      {/* Left Vertical Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentRole={currentRole}
        setCurrentRole={setCurrentRole}
      />

      {/* Main Content Area */}
      <div className="main-wrapper">
        
        {/* Top Context Bar */}
        <TopBar
          activeTab={activeTab}
          lastUpdated={lastUpdated}
          onRefresh={() => loadData(true)}
          isRefreshing={isRefreshing}
        />

        {/* Demo Control Strip (Visible across all tabs) */}
        <DemoControlPanel
          onRefresh={() => loadData(true)}
          onOpenBytesModal={() => setBytesModalOpen(true)}
        />

        {/* Dynamic Main View */}
        <main style={{ flex: 1, minWidth: 0 }}>
          
          {/* 1. Public Portal & DPDP Charter */}
          {activeTab === 'portal' && (
            <PublicPortal onLaunchDashboard={() => setActiveTab('dashboard')} />
          )}

          {/* 2. Overview & Insights Dashboard */}
          {activeTab === 'dashboard' && (
            <DashboardOverview
              kpis={kpis}
              trafficData={trafficData}
              issues={issues}
              workOrders={workOrders}
              onNavigateTab={setActiveTab}
            />
          )}

          {/* 3. GIS Live Map Tab */}
          {activeTab === 'map' && (
            <div style={{
              display: 'flex',
              gap: '20px',
              margin: '20px 28px',
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

          {/* 4. Work Orders Tab */}
          {activeTab === 'work_orders' && (
            <WorkOrdersView
              workOrders={workOrders}
              currentRole={currentRole}
              onRefresh={() => loadData(true)}
              onTriggerDenialModal={(msg) => setDenialModal({ open: true, message: msg })}
            />
          )}

          {/* 5. Traffic Heatmap Tab */}
          {activeTab === 'traffic' && (
            <TrafficView trafficData={trafficData} />
          )}

          {/* 6. Audit Trail Tab */}
          {activeTab === 'audit' && (
            <AuditView currentRole={currentRole} />
          )}

        </main>

      </div>

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
