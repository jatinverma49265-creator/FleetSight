"""Tests for edge centroid tracker."""

from __future__ import annotations

from edge.tracking import CentroidTracker, TrackerConfig
from ml.detector import Detection


def make_detection(
    class_id: int = 0,
    class_name: str = "pothole",
    x1: float = 100.0,
    y1: float = 100.0,
    x2: float = 200.0,
    y2: float = 200.0,
    confidence: float = 0.8,
) -> Detection:
    return Detection(
        class_id=class_id,
        class_name=class_name,
        confidence=confidence,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
    )


class TestCentroidTracker:
    def test_first_frame_registers_tracks(self) -> None:
        tracker = CentroidTracker()
        dets = [make_detection()]
        results = tracker.update(dets)
        assert len(results) == 1
        assert results[0].track_id.startswith("trk_")
        assert tracker.active_track_count == 1

    def test_same_object_keeps_same_track_id(self) -> None:
        tracker = CentroidTracker()
        det1 = make_detection(x1=100.0, y1=100.0, x2=200.0, y2=200.0)
        r1 = tracker.update([det1])
        track_id_first = r1[0].track_id

        # Slightly shifted detection (same object)
        det2 = make_detection(x1=105.0, y1=105.0, x2=205.0, y2=205.0)
        r2 = tracker.update([det2])
        assert r2[0].track_id == track_id_first

    def test_two_separate_objects_get_different_track_ids(self) -> None:
        tracker = CentroidTracker()
        dets = [
            make_detection(x1=0.0, y1=0.0, x2=50.0, y2=50.0),
            make_detection(x1=500.0, y1=500.0, x2=550.0, y2=550.0),
        ]
        results = tracker.update(dets)
        assert len(results) == 2
        assert results[0].track_id != results[1].track_id

    def test_empty_frame_increments_disappeared(self) -> None:
        tracker = CentroidTracker(TrackerConfig(max_disappeared=2))
        tracker.update([make_detection()])
        assert tracker.active_track_count == 1

        tracker.update([])
        assert tracker.active_track_count == 1  # 1 disappeared < max=2

        tracker.update([])
        assert tracker.active_track_count == 1  # 2 disappeared == max=2

        tracker.update([])  # 3 disappeared > max=2, deregistered
        assert tracker.active_track_count == 0

    def test_hits_increment_on_matched_detection(self) -> None:
        tracker = CentroidTracker()
        det = make_detection()
        tracker.update([det])
        track_id = list(tracker._tracks.keys())[0]
        assert tracker._tracks[track_id].hits == 1

        tracker.update([make_detection(x1=102.0, y1=102.0, x2=202.0, y2=202.0)])
        assert tracker._tracks[track_id].hits == 2

    def test_reset_clears_all_tracks(self) -> None:
        tracker = CentroidTracker()
        tracker.update([make_detection()])
        assert tracker.active_track_count == 1
        tracker.reset()
        assert tracker.active_track_count == 0
        assert tracker._next_id == 1

    def test_class_mismatch_creates_new_track(self) -> None:
        """A pothole and a car at the same position should be separate tracks."""
        tracker = CentroidTracker()
        pothole = make_detection(class_id=0, class_name="pothole", x1=100.0, y1=100.0)
        r1 = tracker.update([pothole])
        tid1 = r1[0].track_id

        car = make_detection(class_id=1, class_name="car", x1=100.0, y1=100.0)
        r2 = tracker.update([car])
        assert r2[0].track_id != tid1

    def test_large_distance_creates_new_track(self) -> None:
        """Detection far from existing track should register as new."""
        tracker = CentroidTracker(TrackerConfig(max_distance_px=30.0))
        tracker.update([make_detection(x1=0.0, y1=0.0, x2=50.0, y2=50.0)])
        assert tracker.active_track_count == 1

        r2 = tracker.update([make_detection(x1=500.0, y1=500.0, x2=550.0, y2=550.0)])
        assert tracker.active_track_count == 2
        assert r2[0].track_id != "trk_0001"

    def test_invalid_empty_detections_list(self) -> None:
        tracker = CentroidTracker()
        results = tracker.update([])
        assert results == [] or list(results) == []
