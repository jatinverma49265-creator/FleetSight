"""
FleetSight multi-bus corridor simulation script.

Simulates buses RJ14-01, RJ14-07, and RJ14-12 replaying the Jaipur corridor
(MI Road -> Tonk Road -> JLN Marg -> Civil Lines) with deterministic random seeds,
Gaussian GPS noise, time offsets, offline store-and-forward edge caching, and re-detection verification.
"""

from __future__ import annotations

import argparse
import random
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.analytics.store import store
from backend.schemas import (
    BoundingBox,
    DataOrigin,
    DetectionClass,
    DetectionEvent,
    DetectionType,
    IssueStatus,
    SeverityLevel,
    WorkOrderStatus,
)
from edge.cache import SQLiteEventCache

# Canonical corridor defect reference points
CORRIDOR_DEFECTS = [
    {
        "defect_id": "DEF-POT-01",
        "type": DetectionType.ROAD_DAMAGE,
        "class": DetectionClass.POTHOLE,
        "severity": SeverityLevel.HIGH,
        "base_lat": 26.91720,
        "base_lon": 75.81250,
        "road_segment": "MI Road (Ajmeri Gate to Paanch Batti)",
        "evidence_uri": "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80",
    },
    {
        "defect_id": "DEF-CRK-01",
        "type": DetectionType.ROAD_DAMAGE,
        "class": DetectionClass.ALLIGATOR_CRACK,
        "severity": SeverityLevel.HIGH,
        "base_lat": 26.89100,
        "base_lon": 75.80750,
        "road_segment": "Tonk Road (Rambagh to Gandhi Nagar)",
        "evidence_uri": None,
    },
    {
        "defect_id": "DEF-WTR-01",
        "type": DetectionType.ROAD_DAMAGE,
        "class": DetectionClass.WATERLOGGING,
        "severity": SeverityLevel.CRITICAL,
        "base_lat": 26.88500,
        "base_lon": 75.81500,
        "road_segment": "JLN Marg (Birla Temple to Jawahar Circle)",
        "evidence_uri": None,
    },
    {
        "defect_id": "DEF-BAR-01",
        "type": DetectionType.INFRASTRUCTURE,
        "class": DetectionClass.DAMAGED_BARRIER,
        "severity": SeverityLevel.MEDIUM,
        "base_lat": 26.90800,
        "base_lon": 75.78300,
        "road_segment": "Civil Lines / Ajmer Road",
        "evidence_uri": None,
    },
]


def execute_bus_pass(
    pass_number: int = 1,
    seed: int = 42,
    custom_bus_id: str | None = None,
) -> dict[str, Any]:
    """
    Execute a single corridor pass deterministically.

    - Pass 1 (Bus RJ14-01): Generates initial candidate detections.
    - Pass 2 (Bus RJ14-07): Traverses same corridor with time offset & GPS noise -> triggers 2-bus corroboration to VERIFIED.
    - Pass 3 (Bus RJ14-12): Re-detection survey pass (proposes closure if repaired; escalates if persistent).
    """
    rng = random.Random(seed + pass_number * 100)
    now = datetime.now(UTC)

    bus_map = {1: "RJ14-01", 2: "RJ14-07", 3: "RJ14-12"}
    bus_id = custom_bus_id or bus_map.get(pass_number, f"RJ14-0{pass_number}")
    camera_id = f"CAM-FRONT-0{pass_number}"

    ingested_events: list[str] = []
    affected_issues: list[str] = []

    if pass_number == 1:
        # Pass 1: Bus 01 detects candidates
        defects_to_detect = [CORRIDOR_DEFECTS[0], CORRIDOR_DEFECTS[1], CORRIDOR_DEFECTS[3]]
        for d in defects_to_detect:
            # Deterministic small noise (~3-8m)
            noise_lat = rng.gauss(0, 0.00004)
            noise_lon = rng.gauss(0, 0.00004)
            conf = round(rng.uniform(0.85, 0.94), 2)
            event_id = f"EVT-P1-{d['defect_id']}-{seed}"

            event = DetectionEvent(
                event_id=event_id,
                type=d["type"],
                detection_class=d["class"],
                confidence=conf,
                severity=d["severity"],
                latitude=d["base_lat"] + noise_lat,
                longitude=d["base_lon"] + noise_lon,
                timestamp=now - timedelta(minutes=40),
                camera_id=camera_id,
                bus_id=bus_id,
                model_version="yolo11-v0.1.0",
                evidence_uri=d["evidence_uri"],
                bbox=BoundingBox(x=0.45, y=0.60, w=0.20, h=0.15),
                data_origin=DataOrigin.SIMULATED,
            )
            issue = store.ingest_event(event)
            ingested_events.append(event.event_id)
            if issue:
                affected_issues.append(issue.issue_id)

    elif pass_number == 2:
        # Pass 2: Bus 02 corroborates Pothole & Alligator Crack (~10-15m GPS noise)
        defects_to_detect = [CORRIDOR_DEFECTS[0], CORRIDOR_DEFECTS[1]]
        for d in defects_to_detect:
            noise_lat = rng.gauss(0, 0.00008)
            noise_lon = rng.gauss(0, 0.00008)
            conf = round(rng.uniform(0.88, 0.96), 2)
            event_id = f"EVT-P2-{d['defect_id']}-{seed}"

            event = DetectionEvent(
                event_id=event_id,
                type=d["type"],
                detection_class=d["class"],
                confidence=conf,
                severity=d["severity"],
                latitude=d["base_lat"] + noise_lat,
                longitude=d["base_lon"] + noise_lon,
                timestamp=now - timedelta(minutes=15),
                camera_id=camera_id,
                bus_id=bus_id,
                model_version="yolo11-v0.1.0",
                evidence_uri=d["evidence_uri"],
                bbox=BoundingBox(x=0.42, y=0.58, w=0.22, h=0.16),
                data_origin=DataOrigin.SIMULATED,
            )
            issue = store.ingest_event(event)
            ingested_events.append(event.event_id)
            if issue:
                affected_issues.append(issue.issue_id)

    elif pass_number == 3:
        # Pass 3: Re-detection pass
        # Detects only the Alligator Crack (simulating that the Pothole was repaired, but Crack persists)
        d = CORRIDOR_DEFECTS[1]
        noise_lat = rng.gauss(0, 0.00006)
        noise_lon = rng.gauss(0, 0.00006)
        event_id = f"EVT-P3-{d['defect_id']}-{seed}"
        event = DetectionEvent(
            event_id=event_id,
            type=d["type"],
            detection_class=d["class"],
            confidence=0.90,
            severity=d["severity"],
            latitude=d["base_lat"] + noise_lat,
            longitude=d["base_lon"] + noise_lon,
            timestamp=now - timedelta(minutes=2),
            camera_id=camera_id,
            bus_id=bus_id,
            model_version="yolo11-v0.1.0",
            data_origin=DataOrigin.SIMULATED,
        )
        issue = store.ingest_event(event)
        ingested_events.append(event.event_id)
        if issue:
            affected_issues.append(issue.issue_id)

        # Run re-detection survey check
        detected_issue_ids = [issue.issue_id] if issue else []
        redetection_summary = store.process_redetection_pass(
            bus_id=bus_id,
            detected_issue_ids=detected_issue_ids,
        )
        return {
            "pass_number": pass_number,
            "bus_id": bus_id,
            "events_ingested": len(ingested_events),
            "event_ids": ingested_events,
            "affected_issues": affected_issues,
            "redetection_summary": redetection_summary,
        }

    return {
        "pass_number": pass_number,
        "bus_id": bus_id,
        "events_ingested": len(ingested_events),
        "event_ids": ingested_events,
        "affected_issues": affected_issues,
        "total_issues": len(store.issues),
        "total_work_orders": len(store.work_orders),
    }


def run_offline_store_and_forward_test(seed: int = 42, cache_db: str = ":memory:") -> dict[str, Any]:
    """
    Test edge offline caching during cellular drop and idempotent re-sync.

    1. Caches 5 events into local SQLiteEventCache while network is offline.
    2. Reconnects and syncs all cached events to the central store.
    3. Flushes again to confirm 0 duplicates created.
    """
    cache = SQLiteEventCache(db_path=cache_db)
    now = datetime.now(UTC)

    # Step 1: Queue events offline
    cached_ids = []
    for i in range(5):
        event_id = f"EVT-OFFLINE-{seed}-{i}"
        evt = DetectionEvent(
            event_id=event_id,
            type=DetectionType.ROAD_DAMAGE,
            detection_class=DetectionClass.POTHOLE,
            confidence=0.89,
            latitude=26.91720 + (i * 0.0001),
            longitude=75.81250 + (i * 0.0001),
            timestamp=now - timedelta(minutes=10 - i),
            camera_id="CAM-OFFLINE-01",
            bus_id="RJ14-07",
            model_version="yolo11-v0.1.0",
            data_origin=DataOrigin.SIMULATED,
        )
        cache.push(evt.model_dump(by_alias=True, mode="json"))
        cached_ids.append(event_id)

    assert cache.size == 5, f"Expected 5 cached events, got {cache.size}"

    # Step 2: First Sync (Network Restored)
    events_to_sync = cache.get_pending(limit=10)
    initial_event_count = len(store.events)

    for item in events_to_sync:
        evt = DetectionEvent(**item)
        store.ingest_event(evt)
        cache.mark_synced([item["event_id"]])

    synced_event_count = len(store.events) - initial_event_count

    # Step 3: Re-syncing the same events (Idempotency test)
    for item in events_to_sync:
        evt = DetectionEvent(**item)
        store.ingest_event(evt)

    duplicate_count = len(store.events) - (initial_event_count + synced_event_count)

    return {
        "cached_events_count": 5,
        "synced_events_count": synced_event_count,
        "duplicates_after_resync": duplicate_count,
        "is_idempotent": duplicate_count == 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="FleetSight Multi-Bus Simulator")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for repeatability")
    parser.add_argument("--pass", dest="pass_num", type=int, default=1, choices=[1, 2, 3], help="Bus pass number (1, 2, or 3)")
    parser.add_argument("--offline-test", action="store_true", help="Run offline store-and-forward test")
    parser.add_argument("--run-all", action="store_true", help="Run Pass 1, 2, and 3 consecutively")
    args = parser.parse_args()

    if args.offline_test:
        print(f"Running Offline Store-and-Forward Test (Seed: {args.seed})...")
        res = run_offline_store_and_forward_test(seed=args.seed)
        print(f"Result: {res}")
        if res["is_idempotent"]:
            print("SUCCESS: 0 duplicate records created upon re-sync.")
        return

    if args.run_all:
        print(f"=== Running Full Multi-Bus Corridor Simulation (Seed: {args.seed}) ===")
        store.reset_state()
        
        print("\n--- Pass 1: Bus RJ14-01 (Initial Candidate Detections) ---")
        p1 = execute_bus_pass(pass_number=1, seed=args.seed)
        print(f"Events ingested: {p1['events_ingested']}, Issues created: {p1['total_issues']}")

        print("\n--- Pass 2: Bus RJ14-07 (Multi-Bus Corroboration) ---")
        p2 = execute_bus_pass(pass_number=2, seed=args.seed)
        print(f"Events ingested: {p2['events_ingested']}, Total Issues: {p2['total_issues']}, Work Orders: {p2['total_work_orders']}")

        # Engineer assigns the pothole work order
        wos = store.get_work_orders()
        if wos:
            pothole_wo = wos[0]
            store.update_work_order(
                work_order_id=pothole_wo.work_order_id,
                user=store.users["engineer"],
                status=WorkOrderStatus.COMPLETED,
                comment="Repaired with asphalt patch by Division 1 Crew.",
            )
            print(f"\nPWD Engineer marked {pothole_wo.work_order_id} as COMPLETED (Repaired).")

        print("\n--- Pass 3: Bus RJ14-12 (Automated Re-Detection Loop) ---")
        p3 = execute_bus_pass(pass_number=3, seed=args.seed)
        print(f"Re-detection Summary: {p3['redetection_summary']}")
        print(f"Closed Work Orders (Verified Repaired): {p3['redetection_summary']['closed_work_orders']}")
        print(f"Escalated Work Orders (Persistent): {p3['redetection_summary']['escalated_work_orders']}")
        return

    print(f"Executing Bus Pass {args.pass_num} (Seed: {args.seed})...")
    res = execute_bus_pass(pass_number=args.pass_num, seed=args.seed)
    print(f"Pass {args.pass_num} Result: {res}")


if __name__ == "__main__":
    main()
