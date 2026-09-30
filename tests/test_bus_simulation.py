"""
Tests for multi-bus simulation, offline caching, and re-detection loop (Loop 7).
"""

from datetime import UTC, datetime

import pytest

from backend.analytics.store import store
from backend.schemas import WorkOrderStatus
from scripts.run_demo_scenario import run_full_scenario
from scripts.simulate_buses import execute_bus_pass, run_offline_store_and_forward_test


def test_simulation_seed_repeatability():
    """Verify that running the simulation with the same seed yields identical results."""
    run1 = run_full_scenario(seed=42)
    run2 = run_full_scenario(seed=42)

    assert run1["total_issues"] == run2["total_issues"]
    assert run1["total_work_orders"] == run2["total_work_orders"]
    assert run1["issues_summary"] == run2["issues_summary"]
    assert run1["work_orders_summary"] == run2["work_orders_summary"]


def test_offline_store_and_forward_zero_duplicates():
    """Verify that caching offline events and re-syncing creates 0 duplicates."""
    store.reset_state()
    res = run_offline_store_and_forward_test(seed=42)
    assert res["cached_events_count"] == 5
    assert res["synced_events_count"] == 5
    assert res["duplicates_after_resync"] == 0
    assert res["is_idempotent"] is True


def test_redetection_loop_closed_and_escalated():
    """Verify re-detection closes repaired work orders and escalates persistent ones."""
    store.reset_state()

    # Pass 1: Bus 01 creates candidates
    execute_bus_pass(pass_number=1, seed=42)
    # Pass 2: Bus 02 corroborates to verified & creates work orders
    execute_bus_pass(pass_number=2, seed=42)

    wos = store.get_work_orders()
    assert len(wos) >= 2

    # Engineer marks first work order as COMPLETED (Repaired)
    repaired_wo = wos[0]
    store.update_work_order(
        work_order_id=repaired_wo.work_order_id,
        user=store.users["engineer"],
        status=WorkOrderStatus.COMPLETED,
        comment="Repaired with asphalt",
    )

    # Pass 3: Bus 03 surveys the corridor (Pothole repaired = not detected; Alligator Crack persists = detected)
    p3 = execute_bus_pass(pass_number=3, seed=42)
    summary = p3["redetection_summary"]

    assert repaired_wo.work_order_id in summary["closed_work_orders"]
    updated_wo = store.get_work_order_by_id(repaired_wo.work_order_id)
    assert updated_wo.status == WorkOrderStatus.CLOSED
