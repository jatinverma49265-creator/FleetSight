"""Tests for route- and day-aware dataset splitting and anti-leakage guarantees."""

from __future__ import annotations

from pathlib import Path

import pytest

from ml.datasets.split import RouteDaySplitter, SplitRatio


class TestDatasetSplitter:
    def test_split_ratio_validation(self) -> None:
        ratio = SplitRatio(train=0.70, val=0.15, test=0.15)
        assert ratio.train == 0.70

        with pytest.raises(ValueError, match="Split ratios must sum to 1.0"):
            SplitRatio(train=0.80, val=0.20, test=0.10)

        with pytest.raises(ValueError, match="Split ratios cannot be negative"):
            SplitRatio(train=-0.1, val=0.5, test=0.6)

    def test_empty_frame_list_returns_empty_result(self) -> None:
        splitter = RouteDaySplitter()
        res = splitter.split([])
        assert res.total_frames == 0
        assert len(res.train_ids) == 0

    def test_route_day_anti_leakage(self) -> None:
        """
        Verify that frames belonging to the same (route, day) are NEVER split across
        train, val, or test.
        """
        frames: list[tuple[str, str, str]] = []

        # Create 10 groups of 10 adjacent frames each (total 100 frames)
        for g_idx in range(10):
            route = f"Route-{g_idx % 4}"
            day = f"2026-09-{(g_idx % 3) + 1:02d}"
            for f_idx in range(10):
                frame_id = f"frame_{g_idx}_{f_idx}"
                frames.append((frame_id, route, day))

        splitter = RouteDaySplitter(ratio=SplitRatio(train=0.7, val=0.15, test=0.15), seed=123)
        result = splitter.split(frames)

        assert result.total_frames == 100
        # verify zero intersection
        result.verify_no_leakage()

        # Check that all frames of any (route, day) group belong to exactly one split
        split_assignments: dict[str, str] = {}
        for fid in result.train_ids:
            split_assignments[fid] = "train"
        for fid in result.val_ids:
            split_assignments[fid] = "val"
        for fid in result.test_ids:
            split_assignments[fid] = "test"

        group_splits: dict[str, set[str]] = {}
        for fid, route, day in frames:
            g_key = f"{route}___{day}"
            if g_key not in group_splits:
                group_splits[g_key] = set()
            group_splits[g_key].add(split_assignments[fid])

        # Every group must be in exactly one split partition
        for g_key, splits_seen in group_splits.items():
            assert len(splits_seen) == 1, f"Group {g_key} leaked across splits: {splits_seen}"

    def test_deterministic_split_with_seed(self) -> None:
        frames = [(f"f_{i}", f"R{i % 3}", f"Day{i % 2}") for i in range(30)]
        s1 = RouteDaySplitter(seed=42)
        s2 = RouteDaySplitter(seed=42)
        r1 = s1.split(frames)
        r2 = s2.split(frames)
        assert r1.train_ids == r2.train_ids
        assert r1.val_ids == r2.val_ids
        assert r1.test_ids == r2.test_ids

    def test_save_split_files(self, tmp_path: Path) -> None:
        frames = [(f"f_{i}", f"R{i % 2}", f"Day{i % 2}") for i in range(10)]
        splitter = RouteDaySplitter(seed=42)
        res = splitter.split(frames)

        res.save_to_dir(tmp_path)
        assert (tmp_path / "train.txt").exists()
        assert (tmp_path / "val.txt").exists()
        assert (tmp_path / "test.txt").exists()
