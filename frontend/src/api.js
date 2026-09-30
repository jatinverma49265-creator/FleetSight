/**
 * FleetSight API client for dashboard communication.
 */

const API_BASE = '/api/v1';

export async function fetchKPIs() {
  const res = await fetch(`${API_BASE}/kpis/`);
  if (!res.ok) throw new Error(`Failed to fetch KPIs: ${res.statusText}`);
  return res.json();
}

export async function fetchIssues(status = null, detectionClass = null) {
  const params = new URLSearchParams();
  if (status) params.append('status', status);
  if (detectionClass) params.append('class', detectionClass);
  const res = await fetch(`${API_BASE}/issues/?${params.toString()}`);
  if (!res.ok) throw new Error(`Failed to fetch issues: ${res.statusText}`);
  return res.json();
}

export async function fetchIssueDetail(issueId, userRole = 'viewer') {
  const res = await fetch(`${API_BASE}/issues/${issueId}`, {
    headers: { 'x-user-role': userRole },
  });
  if (!res.ok) throw new Error(`Failed to fetch issue ${issueId}: ${res.statusText}`);
  return res.json();
}

export async function fetchWorkOrders(status = null) {
  const params = new URLSearchParams();
  if (status) params.append('status', status);
  const res = await fetch(`${API_BASE}/work-orders/?${params.toString()}`);
  if (!res.ok) throw new Error(`Failed to fetch work orders: ${res.statusText}`);
  return res.json();
}

export async function updateWorkOrder(workOrderId, { status, assigned_to, comment }, userRole = 'engineer') {
  const res = await fetch(`${API_BASE}/work-orders/${workOrderId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'x-user-role': userRole,
    },
    body: JSON.stringify({ status, assigned_to, comment }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    const err = new Error(errorData.detail || `Action failed with HTTP ${res.status}`);
    err.status = res.status;
    err.detail = errorData.detail;
    throw err;
  }
  return res.json();
}

export async function fetchTraffic() {
  const res = await fetch(`${API_BASE}/traffic/`);
  if (!res.ok) throw new Error(`Failed to fetch traffic data: ${res.statusText}`);
  return res.json();
}

export async function fetchAuditLogs(userRole = 'admin', limit = 50) {
  const res = await fetch(`${API_BASE}/audit/?limit=${limit}`, {
    headers: { 'x-user-role': userRole },
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    const err = new Error(errorData.detail || `Audit access denied (${res.status})`);
    err.status = res.status;
    err.detail = errorData.detail;
    throw err;
  }
  return res.json();
}
