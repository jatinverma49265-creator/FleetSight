"""Tests for SQLite offline event cache and store-and-forward manager."""

from __future__ import annotations

import uuid
from typing import Any

import pytest

from edge.cache import EventStatus, SQLiteEventCache
from edge.sync import MockSyncTransport, StoreAndForwardManager


def make_event(
    event_id: str | None = None,
    bus_id: str = "BUS-001",
    detection_class: str = "pothole",
) -> dict[str, Any]:
    return {
        "event_id": event_id or str(uuid.uuid4()),
        "bus_id": bus_id,
        "class": detection_class,
        "confidence": 0.85,
        "latitude": 26.9,
        "longitude": 75.8,
        "timestamp": "2024-01-01T00:00:00+00:00",
        "camera_id": "CAM-01",
        "model_version": "yolo11-v0.1.0",
    }


class TestSQLiteEventCache:
    def setup_method(self) -> None:
        self.cache = SQLiteEventCache(db_path=":memory:")

    def teardown_method(self) -> None:
        self.cache.close()

    def test_push_and_get_pending(self) -> None:
        ev = make_event()
        self.cache.push(ev)
        pending = self.cache.get_pending()
        assert len(pending) == 1
        assert pending[0]["event_id"] == ev["event_id"]

    def test_size_counts_pending_and_failed(self) -> None:
        ev1 = make_event()
        ev2 = make_event()
        self.cache.push(ev1)
        self.cache.push(ev2)
        assert self.cache.size == 2

    def test_total_count_includes_all_statuses(self) -> None:
        ev = make_event()
        self.cache.push(ev)
        self.cache.mark_synced([ev["event_id"]])
        assert self.cache.total_count == 1
        assert self.cache.size == 0  # synced not counted in size

    def test_mark_synced_removes_from_pending(self) -> None:
        ev = make_event()
        self.cache.push(ev)
        self.cache.mark_synced([ev["event_id"]])
        assert self.cache.get_pending() == []

    def test_mark_failed_updates_status_and_retry_count(self) -> None:
        ev = make_event()
        self.cache.push(ev)
        self.cache.mark_failed(ev["event_id"], "Network timeout")
        record = self.cache.get_event(ev["event_id"])
        assert record is not None
        assert record["status"] == EventStatus.FAILED
        assert record["retry_count"] == 1
        assert "Network timeout" in record["last_error"]

    def test_get_event_by_id(self) -> None:
        ev = make_event()
        self.cache.push(ev)
        record = self.cache.get_event(ev["event_id"])
        assert record is not None
        assert record["payload"]["event_id"] == ev["event_id"]

    def test_get_event_missing_returns_none(self) -> None:
        result = self.cache.get_event("nonexistent-id")
        assert result is None

    def test_flush_returns_and_removes_pending(self) -> None:
        ev1 = make_event()
        ev2 = make_event()
        self.cache.push(ev1)
        self.cache.push(ev2)
        flushed = self.cache.flush()
        assert len(flushed) == 2
        assert self.cache.size == 0

    def test_push_without_event_id_raises(self) -> None:
        from edge.exceptions import CacheError

        with pytest.raises(CacheError, match="event_id"):
            self.cache.push({"bus_id": "BUS-001"})

    def test_duplicate_push_replaces_existing(self) -> None:
        eid = str(uuid.uuid4())
        ev = make_event(event_id=eid)
        self.cache.push(ev)
        # Push same event again (e.g. retry) — INSERT OR REPLACE
        self.cache.push(ev)
        assert self.cache.total_count == 1

    def test_get_pending_respects_limit(self) -> None:
        for _ in range(10):
            self.cache.push(make_event())
        pending = self.cache.get_pending(limit=3)
        assert len(pending) == 3


class TestMockSyncTransport:
    def test_sync_event_success(self) -> None:
        transport = MockSyncTransport(should_succeed=True)
        ev = make_event()
        result = transport.sync_event(ev)
        assert result is True
        assert len(transport.synced_events) == 1

    def test_sync_event_failure(self) -> None:
        transport = MockSyncTransport(should_succeed=False)
        ev = make_event()
        result = transport.sync_event(ev)
        assert result is False
        assert len(transport.failed_events) == 1

    def test_sync_batch_returns_ids(self) -> None:
        transport = MockSyncTransport(should_succeed=True)
        events = [make_event(), make_event()]
        success_ids, failed_ids = transport.sync_batch(events)
        assert len(success_ids) == 2
        assert len(failed_ids) == 0

    def test_sync_attempts_counted(self) -> None:
        transport = MockSyncTransport()
        transport.sync_event(make_event())
        transport.sync_event(make_event())
        assert transport.sync_attempts == 2


class TestStoreAndForwardManager:
    def setup_method(self) -> None:
        self.cache = SQLiteEventCache(db_path=":memory:")

    def teardown_method(self) -> None:
        self.cache.close()

    def test_successful_sync_marks_events_synced(self) -> None:
        ev = make_event()
        self.cache.push(ev)
        transport = MockSyncTransport(should_succeed=True)
        manager = StoreAndForwardManager(self.cache, transport)
        success, failed = manager.sync_pending()
        assert success == 1
        assert failed == 0
        assert self.cache.size == 0

    def test_failed_sync_marks_events_failed(self) -> None:
        ev = make_event()
        self.cache.push(ev)
        transport = MockSyncTransport(should_succeed=False)
        manager = StoreAndForwardManager(self.cache, transport)
        success, failed = manager.sync_pending()
        assert success == 0
        assert failed == 1
        # Event still counted in size (failed state)
        assert self.cache.size == 1
        record = self.cache.get_event(ev["event_id"])
        assert record is not None
        assert record["status"] == EventStatus.FAILED

    def test_empty_cache_returns_zero_counts(self) -> None:
        transport = MockSyncTransport()
        manager = StoreAndForwardManager(self.cache, transport)
        success, failed = manager.sync_pending()
        assert success == 0
        assert failed == 0

    def test_batch_size_limits_sync_batch(self) -> None:
        for _ in range(10):
            self.cache.push(make_event())
        transport = MockSyncTransport(should_succeed=True)
        manager = StoreAndForwardManager(self.cache, transport, batch_size=3)
        success, failed = manager.sync_pending()
        assert success == 3
        # Remaining 7 still pending
        assert self.cache.size == 7
