"""
SQLite Offline Event Cache.

Lightweight, atomic local persistence for buffering detection events on the bus
during intermittent or offline cellular connectivity.
Stores structured metadata and evidence file references only (no large binaries).
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Sequence
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from edge.exceptions import CacheError
from edge.interfaces import EventCache


class EventStatus(StrEnum):
    """Lifecycle status of an edge event."""

    PENDING = "pending"
    SYNCED = "synced"
    FAILED = "failed"


class SQLiteEventCache(EventCache):
    """
    Local SQLite event store implementing EventCache protocol.
    """

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.db_path = str(db_path)
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        """Create schema if not exists."""
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS edge_events (
                    event_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    synced_at TEXT,
                    bus_id TEXT NOT NULL,
                    detection_class TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    evidence_path TEXT,
                    retry_count INTEGER DEFAULT 0,
                    last_error TEXT
                )
                """
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_edge_status ON edge_events(status)"
            )

    @property
    def size(self) -> int:
        """Total number of pending or failed events waiting for synchronization."""
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM edge_events WHERE status IN ('pending', 'failed')"
        )
        row = cursor.fetchone()
        return int(row[0]) if row else 0

    @property
    def total_count(self) -> int:
        """Total count of all recorded events in the database."""
        cursor = self._conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM edge_events")
        row = cursor.fetchone()
        return int(row[0]) if row else 0

    def push(self, event: dict[str, Any]) -> None:
        """
        Atomically persist a candidate detection event into local cache.

        Raises:
            CacheError: If event_id is missing or database insertion fails.
        """
        event_id = event.get("event_id")
        if not event_id:
            raise CacheError("Cannot push event without an 'event_id'")

        bus_id = str(event.get("bus_id", "UNKNOWN"))
        det_class = str(event.get("class", event.get("detection_class", "unknown")))
        evidence_path = event.get("evidence_uri")
        created_at = event.get("timestamp", datetime.now(UTC).isoformat())
        payload_json = json.dumps(event)

        try:
            with self._conn:
                self._conn.execute(
                    """
                    INSERT OR REPLACE INTO edge_events
                    (event_id, status, created_at, bus_id,
                     detection_class, payload, evidence_path, retry_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                    """,
                    (
                        str(event_id),
                        EventStatus.PENDING.value,
                        str(created_at),
                        bus_id,
                        det_class,
                        payload_json,
                        evidence_path,
                    ),
                )
        except Exception as e:
            raise CacheError(f"Failed to persist event '{event_id}': {e}") from e

    def get_pending(self, limit: int = 50) -> list[dict[str, Any]]:
        """Retrieve up to limit oldest pending events."""
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT payload FROM edge_events
            WHERE status = 'pending'
            ORDER BY created_at ASC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        return [json.loads(row["payload"]) for row in rows]

    def mark_synced(self, event_ids: Sequence[str]) -> None:
        """Mark events as successfully synced to the central backend."""
        if not event_ids:
            return
        now_str = datetime.now(UTC).isoformat()
        with self._conn:
            self._conn.executemany(
                """
                UPDATE edge_events
                SET status = ?, synced_at = ?
                WHERE event_id = ?
                """,
                [(EventStatus.SYNCED.value, now_str, eid) for eid in event_ids],
            )

    def mark_failed(self, event_id: str, error_message: str) -> None:
        """Increment retry count and record error details."""
        with self._conn:
            self._conn.execute(
                """
                UPDATE edge_events
                SET status = ?, retry_count = retry_count + 1, last_error = ?
                WHERE event_id = ?
                """,
                (EventStatus.FAILED.value, error_message, event_id),
            )

    def get_event(self, event_id: str) -> dict[str, Any] | None:
        """Fetch event record by ID."""
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM edge_events WHERE event_id = ?", (event_id,))
        row = cursor.fetchone()
        if not row:
            return None
        res = dict(row)
        res["payload"] = json.loads(res["payload"])
        return res

    def flush(self) -> list[dict[str, Any]]:
        """Return and remove all cached pending events."""
        pending = self.get_pending(limit=1000)
        with self._conn:
            self._conn.execute("DELETE FROM edge_events WHERE status = 'pending'")
        return pending

    def close(self) -> None:
        """Close SQLite database connection."""
        import contextlib

        with contextlib.suppress(Exception):
            self._conn.close()
