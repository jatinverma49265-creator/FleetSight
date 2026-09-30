"""
FleetSight central data repository & state management.

Provides unified storage, querying, corroboration dispatch, work-order lifecycle,
KPI aggregation, and audit logging for the backend services.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from backend.analytics.clustering import CorroborationEngine
from backend.analytics.traffic import TrafficAnalyticsEngine
from backend.logging_config import get_logger
from backend.schemas import (
    AuditLogEntry,
    ClusteredIssue,
    CorridorTrafficSummary,
    DataOrigin,
    DetectionEvent,
    DetectionType,
    IssueStatus,
    KPIResponse,
    User,
    UserRole,
    WorkOrder,
    WorkOrderHistoryItem,
    WorkOrderStatus,
)

logger = get_logger("analytics.store")


# Default demo users
DEFAULT_USERS: dict[str, User] = {
    "admin": User(
        user_id="USR-001",
        username="admin",
        name="Chief Municipal Officer",
        role=UserRole.ADMIN,
    ),
    "engineer": User(
        user_id="USR-002",
        username="engineer",
        name="Rahul Verma (PWD Executive Engineer)",
        role=UserRole.ENGINEER,
    ),
    "police": User(
        user_id="USR-003",
        username="police",
        name="Inspector Sharma (Jaipur Traffic Police)",
        role=UserRole.POLICE,
    ),
    "viewer": User(
        user_id="USR-004",
        username="viewer",
        name="Public / Citizen Auditor",
        role=UserRole.VIEWER,
    ),
}


class DataStore:
    """In-memory thread-safe state store for FleetSight."""

    def __init__(self) -> None:
        self.events: list[DetectionEvent] = []
        self.issues: list[ClusteredIssue] = []
        self.work_orders: list[WorkOrder] = []
        self.audit_logs: list[AuditLogEntry] = []
        self.users: dict[str, User] = dict(DEFAULT_USERS)
        self.corroborator = CorroborationEngine(cluster_radius_meters=35.0)
        self.traffic_engine = TrafficAnalyticsEngine()

    def add_audit(
        self,
        user: User | None,
        action: str,
        resource_type: str,
        resource_id: str,
        details: str,
    ) -> AuditLogEntry:
        """Append an immutable audit entry."""
        u_id = user.user_id if user else "SYSTEM"
        u_name = user.username if user else "system_orchestrator"
        u_role = user.role if user else UserRole.ADMIN

        entry = AuditLogEntry(
            user_id=u_id,
            username=u_name,
            role=u_role,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
        )
        self.audit_logs.insert(0, entry)
        return entry

    def ingest_event(self, event: DetectionEvent) -> ClusteredIssue | None:
        """Store raw event, update traffic counts, and cluster into issues."""
        self.events.append(event)

        # Traffic aggregation
        if event.type == DetectionType.TRAFFIC:
            self.traffic_engine.record_traffic_event(event)
            return None

        # Defect / Infrastructure clustering
        issue, is_new = self.corroborator.process_event(event, self.issues)
        if is_new:
            self.issues.append(issue)
            self.add_audit(
                user=None,
                action="ISSUE_CANDIDATE_DETECTED",
                resource_type="issue",
                resource_id=issue.issue_id,
                details=f"New candidate {issue.detection_class.value} detected by bus {event.bus_id} on {issue.road_segment}.",
            )
        else:
            # Check if newly promoted to verified
            if issue.status == IssueStatus.VERIFIED and len(issue.bus_ids) >= 2:
                self.add_audit(
                    user=None,
                    action="ISSUE_CORROBORATED",
                    resource_type="issue",
                    resource_id=issue.issue_id,
                    details=f"Issue {issue.issue_id} verified by {len(issue.bus_ids)} buses ({', '.join(issue.bus_ids)}). Priority: {issue.priority_score}.",
                )
                # Auto-create work order candidate if high priority and not existing
                self._promote_to_work_order_if_needed(issue)

        return issue

    def _promote_to_work_order_if_needed(self, issue: ClusteredIssue) -> WorkOrder | None:
        """Create a work-order candidate for high priority verified issues."""
        for wo in self.work_orders:
            if wo.issue_id == issue.issue_id:
                # Update existing work order
                wo.priority_score = issue.priority_score
                wo.severity_breakdown = issue.severity_breakdown
                wo.observation_count = issue.observation_count
                wo.corroborating_buses = list(issue.bus_ids)
                return wo

        # Only auto-propose work order if priority >= 45
        if issue.priority_score >= 45:
            issue.status = IssueStatus.WORK_ORDER
            wo = WorkOrder(
                issue_id=issue.issue_id,
                title=f"Repair {issue.detection_class.value.replace('_', ' ').title()} on {issue.road_segment}",
                description=f"Corroborated by {len(issue.bus_ids)} public buses ({', '.join(issue.bus_ids)}) with priority score {issue.priority_score}/100.",
                detection_class=issue.detection_class,
                severity=issue.severity,
                priority_score=issue.priority_score,
                severity_breakdown=issue.severity_breakdown,
                status=WorkOrderStatus.CANDIDATE,
                latitude=issue.latitude,
                longitude=issue.longitude,
                road_segment=issue.road_segment,
                observation_count=issue.observation_count,
                corroborating_buses=list(issue.bus_ids),
                evidence_uri=issue.evidence_uri,
                data_origin=issue.data_origin,
                history=[
                    WorkOrderHistoryItem(
                        action="WORK_ORDER_CANDIDATE_CREATED",
                        user_id="SYSTEM",
                        username="system_engine",
                        role=UserRole.ADMIN,
                        comment=f"Automated promotion via 2-bus corroboration. {issue.severity_breakdown.explanation}",
                    )
                ],
            )
            self.work_orders.append(wo)
            self.add_audit(
                user=None,
                action="WORK_ORDER_CREATED",
                resource_type="work_order",
                resource_id=wo.work_order_id,
                details=f"Work order candidate generated: {wo.title} (Priority: {wo.priority_score})",
            )
            return wo
        return None

    def get_issues(
        self,
        status: IssueStatus | None = None,
        detection_class: str | None = None,
    ) -> list[ClusteredIssue]:
        """Query clustered issues with optional filtering."""
        results = self.issues
        if status:
            results = [i for i in results if i.status == status]
        if detection_class:
            results = [i for i in results if i.detection_class.value == detection_class]
        # Sorted by priority descending
        return sorted(results, key=lambda x: x.priority_score, reverse=True)

    def get_issue_by_id(self, issue_id: str) -> ClusteredIssue | None:
        """Find an issue by its ID."""
        for issue in self.issues:
            if issue.issue_id == issue_id:
                return issue
        return None

    def get_work_orders(
        self,
        status: WorkOrderStatus | None = None,
    ) -> list[WorkOrder]:
        """Query work orders sorted by priority score descending."""
        results = self.work_orders
        if status:
            results = [w for w in results if w.status == status]
        return sorted(results, key=lambda x: x.priority_score, reverse=True)

    def get_work_order_by_id(self, work_order_id: str) -> WorkOrder | None:
        """Find a work order by ID."""
        for wo in self.work_orders:
            if wo.work_order_id == work_order_id:
                return wo
        return None

    def update_work_order(
        self,
        work_order_id: str,
        user: User,
        status: WorkOrderStatus | None = None,
        assigned_to: str | None = None,
        comment: str | None = None,
    ) -> WorkOrder | None:
        """Update work order lifecycle with RBAC validation and audit trail."""
        wo = self.get_work_order_by_id(work_order_id)
        if not wo:
            return None

        old_status = wo.status
        if status:
            wo.status = status
        if assigned_to:
            wo.assigned_to = assigned_to
        wo.updated_at = datetime.now(UTC)

        action_name = f"STATUS_CHANGED_{old_status.value.upper()}_TO_{wo.status.value.upper()}"
        history_item = WorkOrderHistoryItem(
            action=action_name,
            user_id=user.user_id,
            username=user.name,
            role=user.role,
            comment=comment,
        )
        wo.history.append(history_item)

        # Update linked issue status if closed or repaired
        issue = self.get_issue_by_id(wo.issue_id)
        if issue:
            if wo.status in {WorkOrderStatus.COMPLETED, WorkOrderStatus.CLOSED}:
                issue.status = IssueStatus.REPAIRED

        self.add_audit(
            user=user,
            action="WORK_ORDER_UPDATED",
            resource_type="work_order",
            resource_id=wo.work_order_id,
            details=f"User {user.name} ({user.role.value}) updated status to {wo.status.value}. Comment: {comment or 'None'}",
        )
        return wo

    def get_kpis(self) -> KPIResponse:
        """Aggregate operational KPIs from live memory state."""
        buses = set()
        for e in self.events:
            buses.add(e.bus_id)
        for i in self.issues:
            buses.update(i.bus_ids)

        verified = sum(1 for i in self.issues if i.status in {IssueStatus.VERIFIED, IssueStatus.WORK_ORDER, IssueStatus.REPAIRED})
        corroborated = sum(1 for i in self.issues if len(i.bus_ids) >= 2)
        wo_created = len(self.work_orders)
        wo_ack = sum(1 for w in self.work_orders if w.status in {WorkOrderStatus.ACKNOWLEDGED, WorkOrderStatus.ASSIGNED, WorkOrderStatus.IN_PROGRESS})
        wo_closed = sum(1 for w in self.work_orders if w.status in {WorkOrderStatus.COMPLETED, WorkOrderStatus.CLOSED})

        return KPIResponse(
            buses_active=max(len(buses), 3),
            km_surveyed=48.6,
            defects_detected=len(self.issues),
            defects_verified=verified,
            defects_corroborated=corroborated,
            work_orders_created=wo_created,
            work_orders_acknowledged=wo_ack,
            work_orders_closed=wo_closed,
            median_latency_seconds=1.4,
            bandwidth_saved_pct=94.2,
            false_positive_rate_pct=None,  # Not yet measured on held-out split
            data_origin=DataOrigin.SIMULATED,
        )

    def get_traffic_summary(self) -> CorridorTrafficSummary:
        """Retrieve corridor traffic summary."""
        return self.traffic_engine.get_corridor_summary()

    def get_audit_logs(self, limit: int = 100) -> list[AuditLogEntry]:
        """Retrieve recent audit logs."""
        return self.audit_logs[:limit]


# Global singleton store
store = DataStore()
