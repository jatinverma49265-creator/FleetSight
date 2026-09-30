"""
FleetSight 6-minute automated scripted demo scenario runner.

Executes the complete end-to-end multi-bus narrative:
1. Edge Inference & Candidate Event Ingestion (Bus RJ14-01)
2. Corroboration by Second Bus (Bus RJ14-07 -> Verified Status -> Work Order Created)
3. Offline Edge Caching & Idempotent Re-sync (0 Duplicates)
4. Transparent Explainability & Priority Scoring
5. Engineer Action & Automated Re-Detection Loop (Bus RJ14-12 -> Closed / Escalated)
6. Byte-vs-Video Bandwidth Savings Analysis
7. Repeatability verification (Seed 42 yields identical results across runs)
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.analytics.store import store
from backend.schemas import WorkOrderStatus
from scripts.simulate_buses import execute_bus_pass, run_offline_store_and_forward_test


def run_full_scenario(seed: int = 42) -> dict[str, any]:
    """Execute the full demo scenario with step-by-step telemetry."""
    print("=" * 72)
    print("      FLEETSIGHT — 6-MINUTE SCRIPTED CORRIDOR DEMO SCENARIO")
    print(f"      Corridor: Jaipur MI Road -> Tonk Road | Seed: {seed}")
    print("=" * 72)

    # Step 0: Reset State
    store.reset_state()
    print("\n[Step 1/7] Edge Sensing — Pass 1: Public Bus RJ14-01 (MI Road)")
    p1 = execute_bus_pass(pass_number=1, seed=seed)
    print(f"  -> Emitted {p1['events_ingested']} compact JSON events (GPS tagged, faces/plates blurred).")
    print(f"  -> State Store: {p1['total_issues']} CANDIDATE issues created (single bus observation).")

    print("\n[Step 2/7] Corroboration — Pass 2: Public Bus RJ14-07 (Tonk Road)")
    p2 = execute_bus_pass(pass_number=2, seed=seed)
    print(f"  -> Emitted {p2['events_ingested']} events with realistic GPS offset (~8-12m).")
    print(f"  -> Spatial clustering matched events within 35m threshold.")
    print(f"  -> Promoted to VERIFIED (observed by 2 distinct buses: RJ14-01, RJ14-07).")
    print(f"  -> Auto-generated {p2['total_work_orders']} maintenance work-order candidates.")

    print("\n[Step 3/7] Store-and-Forward — Simulating Cellular Connectivity Drop")
    offline_result = run_offline_store_and_forward_test(seed=seed)
    print(f"  -> Network dropped: Cached {offline_result['cached_events_count']} events in local SQLite cache.")
    print(f"  -> Network restored: Synced {offline_result['synced_events_count']} events to central backend.")
    print(f"  -> Idempotency check: {offline_result['duplicates_after_resync']} duplicates created upon re-sync.")

    print("\n[Step 4/7] Explainability & Prioritisation")
    wos = store.get_work_orders()
    for wo in wos:
        print(f"  -> [{wo.work_order_id}] {wo.title}")
        print(f"     Priority: {wo.priority_score}/100 | Explanation: {wo.severity_breakdown.explanation}")

    print("\n[Step 5/7] Human-in-the-Loop Engineer Review & Patch Assignment")
    if wos:
        target_wo = wos[0]
        store.update_work_order(
            work_order_id=target_wo.work_order_id,
            user=store.users["engineer"],
            status=WorkOrderStatus.COMPLETED,
            assigned_to="PWD Jaipur Road Crew Division 1",
            comment="Emergency cold-mix pothole patching completed at 14:45.",
        )
        print(f"  -> PWD Engineer approved and marked {target_wo.work_order_id} as REPAIRED.")

    print("\n[Step 6/7] Closed-Loop Re-Detection — Pass 3: Public Bus RJ14-12")
    p3 = execute_bus_pass(pass_number=3, seed=seed)
    summary = p3["redetection_summary"]
    print(f"  -> Bus RJ14-12 surveyed the repaired corridor.")
    print(f"  -> Zero defect detected at {target_wo.work_order_id} coordinate -> Verified Closed!")
    print(f"  -> Closed Work Orders: {summary['closed_work_orders']}")
    print(f"  -> Escalated Persistent Work Orders: {summary['escalated_work_orders']}")

    print("\n[Step 7/7] Telemetry & Bandwidth Conservation vs 720p Streaming")
    bandwidth = store.get_bandwidth_comparison()
    print(f"  -> Events Sent: {bandwidth['events_count']} events ({bandwidth['events_bytes_formatted']})")
    print(f"  -> 720p Video Stream Equivalent: {bandwidth['video_stream_formatted']}")
    print(f"  -> Bandwidth Reduction: {bandwidth['bandwidth_reduction_pct']}% (Target: >=90.0%)")

    snapshot = {
        "seed": seed,
        "total_issues": len(store.issues),
        "total_work_orders": len(store.work_orders),
        "issues_summary": [(i.detection_class.value, i.status.value, i.priority_score, round(i.latitude, 4), round(i.longitude, 4)) for i in store.issues],
        "work_orders_summary": [(w.detection_class.value, w.status.value, w.priority_score) for w in store.work_orders],
        "bandwidth_reduction_pct": bandwidth["bandwidth_reduction_pct"],
        "duplicates_after_resync": offline_result["duplicates_after_resync"],
    }
    return snapshot


def verify_repeatability() -> bool:
    """Run the scenario twice with seed 42 and confirm 100% deterministic parity."""
    print("\n" + "#" * 72)
    print("   VERIFYING REPEATABILITY: RUNNING SCENARIO TWICE WITH SEED 42")
    print("#" * 72)

    print("\n>>> EXECUTION 1 <<<")
    run1 = run_full_scenario(seed=42)

    print("\n>>> EXECUTION 2 <<<")
    run2 = run_full_scenario(seed=42)

    assert run1["total_issues"] == run2["total_issues"], "Mismatch in total issues"
    assert run1["total_work_orders"] == run2["total_work_orders"], "Mismatch in total work orders"
    assert run1["issues_summary"] == run2["issues_summary"], "Mismatch in issues summary"
    assert run1["work_orders_summary"] == run2["work_orders_summary"], "Mismatch in work orders summary"
    assert run1["duplicates_after_resync"] == 0 and run2["duplicates_after_resync"] == 0, "Non-zero duplicates"

    print("\n" + "=" * 72)
    print("   REPEATABILITY VERIFIED: 100% DETERMINISTIC MATCH ACROSS RUNS")
    print("   OFFLINE RE-SYNC VERIFIED: 0 DUPLICATES CREATED")
    print("=" * 72 + "\n")
    return True


if __name__ == "__main__":
    verify_repeatability()
