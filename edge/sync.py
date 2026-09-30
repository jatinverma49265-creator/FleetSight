"""
Store-and-Forward Synchronization Subsystem.

Dispatches cached edge events to the central FleetSight ingestion endpoint
when connectivity is confirmed. Guarantees that events are only marked as synced
once the transport layer verifies acceptance.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from edge.cache import SQLiteEventCache
from edge.interfaces import SyncTransport


class MockSyncTransport(SyncTransport):
    """
    In-memory mock transport for testing offline store-and-forward cycles.

    Allows tests to simulate intermittent cellular drops and partial batch failures.
    """

    def __init__(self, should_succeed: bool = True) -> None:
        self.should_succeed = should_succeed
        self.synced_events: list[dict[str, Any]] = []
        self.failed_events: list[dict[str, Any]] = []
        self.sync_attempts: int = 0

    def sync_event(self, event: dict[str, Any]) -> bool:
        """Transmit a single event."""
        self.sync_attempts += 1
        if self.should_succeed:
            self.synced_events.append(event)
            return True
        self.failed_events.append(event)
        return False

    def sync_batch(
        self, events: Sequence[dict[str, Any]]
    ) -> tuple[list[str], list[str]]:
        """Transmit a batch of events, returning (success_ids, failed_ids)."""
        success_ids: list[str] = []
        failed_ids: list[str] = []

        for e in events:
            eid = str(e.get("event_id", ""))
            if self.sync_event(e):
                success_ids.append(eid)
            else:
                failed_ids.append(eid)

        return success_ids, failed_ids


class StoreAndForwardManager:
    """
    Coordinates opportunistic flushing of pending events from SQLite cache to transport.
    """

    def __init__(
        self,
        cache: SQLiteEventCache,
        transport: SyncTransport,
        batch_size: int = 50,
    ) -> None:
        self.cache = cache
        self.transport = transport
        self.batch_size = batch_size

    def sync_pending(self) -> tuple[int, int]:
        """
        Poll pending events and attempt upload via transport.

        Returns:
            (success_count, failure_count)
        """
        pending = self.cache.get_pending(limit=self.batch_size)
        if not pending:
            return 0, 0

        success_ids, failed_ids = self.transport.sync_batch(pending)

        if success_ids:
            self.cache.mark_synced(success_ids)

        for fid in failed_ids:
            self.cache.mark_failed(fid, "Transport dispatch failed or connection refused")

        return len(success_ids), len(failed_ids)
