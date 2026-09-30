"""
Route- and Day-Aware Dataset Splitter.

Prevents spatio-temporal data leakage in continuous dashcam footage by partitioning
frames strictly at the (route_id, capture_day) group level rather than random frame sampling.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SplitRatio:
    """Proportion split configuration. Must sum to 1.0."""

    train: float = 0.70
    val: float = 0.15
    test: float = 0.15
    def __post_init__(self) -> None:
        total = round(self.train + self.val + self.test, 6)
        if total != 1.0:
            ratios_str = f"{self.train} + {self.val} + {self.test} = {total}"
            raise ValueError(f"Split ratios must sum to 1.0; got {ratios_str}")




        if any(r < 0.0 for r in (self.train, self.val, self.test)):
            raise ValueError("Split ratios cannot be negative")


@dataclass
class SplitResult:
    """Result of partitioning frames by group."""

    train_ids: list[str] = field(default_factory=list)
    val_ids: list[str] = field(default_factory=list)
    test_ids: list[str] = field(default_factory=list)
    group_distribution: dict[str, list[str]] = field(default_factory=dict)

    @property
    def total_frames(self) -> int:
        return len(self.train_ids) + len(self.val_ids) + len(self.test_ids)

    def verify_no_leakage(self) -> None:
        """Assert zero intersection between train, val, and test frame ID sets."""
        s_train, s_val, s_test = set(self.train_ids), set(self.val_ids), set(self.test_ids)
        if s_train & s_val:
            raise ValueError(f"Leakage detected between train and val: {s_train & s_val}")
        if s_train & s_test:
            raise ValueError(f"Leakage detected between train and test: {s_train & s_test}")
        if s_val & s_test:
            raise ValueError(f"Leakage detected between val and test: {s_val & s_test}")

    def save_to_dir(self, output_dir: Path | str) -> None:
        """Write train.txt, val.txt, and test.txt index files to output_dir."""
        dest = Path(output_dir)
        dest.mkdir(parents=True, exist_ok=True)
        for name, ids in [
            ("train.txt", self.train_ids),
            ("val.txt", self.val_ids),
            ("test.txt", self.test_ids),
        ]:
            file_path = dest / name
            with file_path.open("w", encoding="utf-8") as f:
                f.write("\n".join(ids) + ("\n" if ids else ""))


class RouteDaySplitter:
    """
    Partitions dashcam frame collections into train/val/test splits
    grouped by (route_id, capture_day).
    """

    def __init__(self, ratio: SplitRatio | None = None, seed: int = 42) -> None:
        self.ratio = ratio or SplitRatio()
        self.seed = seed

    def _group_hash(self, group_key: str) -> float:
        """Deterministic pseudo-random float in [0.0, 1.0) derived from group key and seed."""
        key = f"{self.seed}:{group_key}"
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        # Take first 8 bytes and map to [0, 1)
        int_val = int(digest[:16], 16)
        return int_val / float(1 << 64)

    def split(
        self,
        frames: Sequence[tuple[str, str, str]],
    ) -> SplitResult:
        """
        Group frames by (route_id, capture_day) and assign whole groups to splits.

        Args:
            frames: Sequence of (frame_id, route_id, capture_day) tuples.

        Returns:
            SplitResult with train_ids, val_ids, test_ids.
        """
        if not frames:
            return SplitResult()

        # Group frames by composite key: f"{route_id}_{capture_day}"
        groups: dict[str, list[str]] = defaultdict(list)
        for frame_id, route_id, capture_day in frames:
            group_key = f"{route_id}___{capture_day}"
            groups[group_key].append(frame_id)

        train_ids: list[str] = []
        val_ids: list[str] = []
        test_ids: list[str] = []
        group_distribution: dict[str, list[str]] = {
            "train": [],
            "val": [],
            "test": [],
        }

        # Deterministically assign groups based on hash threshold
        threshold_train = self.ratio.train
        threshold_val = self.ratio.train + self.ratio.val

        sorted_groups = sorted(groups.keys())
        for group_key in sorted_groups:
            score = self._group_hash(group_key)
            if score < threshold_train:
                train_ids.extend(groups[group_key])
                group_distribution["train"].append(group_key)
            elif score < threshold_val:
                val_ids.extend(groups[group_key])
                group_distribution["val"].append(group_key)
            else:
                test_ids.extend(groups[group_key])
                group_distribution["test"].append(group_key)

        result = SplitResult(
            train_ids=train_ids,
            val_ids=val_ids,
            test_ids=test_ids,
            group_distribution=group_distribution,
        )
        result.verify_no_leakage()
        return result
