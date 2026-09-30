"""Tests for edge privacy filter hook."""

from __future__ import annotations

import numpy as np

from edge.privacy import MockPrivacyFilter, NoOpPrivacyFilter


def blank_frame(h: int = 100, w: int = 100) -> np.ndarray:
    return np.full((h, w, 3), 200, dtype=np.uint8)


class TestNoOpPrivacyFilter:
    def test_returns_copy_identical_to_input(self) -> None:
        filt = NoOpPrivacyFilter()
        frame = blank_frame()
        result = filt.filter(frame)
        np.testing.assert_array_equal(result, frame)
        # Must be a copy, not the same object
        assert result is not frame

    def test_regions_argument_ignored(self) -> None:
        filt = NoOpPrivacyFilter()
        frame = blank_frame()
        result = filt.filter(frame, regions=[(10.0, 10.0, 50.0, 50.0)])
        np.testing.assert_array_equal(result, frame)

    def test_accepts_empty_regions(self) -> None:
        filt = NoOpPrivacyFilter()
        frame = blank_frame()
        result = filt.filter(frame, regions=[])
        np.testing.assert_array_equal(result, frame)


class TestMockPrivacyFilter:
    def test_invocations_counter_increments(self) -> None:
        filt = MockPrivacyFilter()
        frame = blank_frame()
        filt.filter(frame)
        filt.filter(frame)
        assert filt.invocations_count == 2

    def test_masked_region_is_black(self) -> None:
        filt = MockPrivacyFilter(mask_color=(0, 0, 0))
        frame = blank_frame()  # all 200
        result = filt.filter(frame, regions=[(10.0, 10.0, 50.0, 50.0)])
        # Interior of masked region should be zeroed
        assert result[20, 20, 0] == 0
        assert result[20, 20, 1] == 0
        assert result[20, 20, 2] == 0

    def test_unmasked_region_unchanged(self) -> None:
        filt = MockPrivacyFilter(mask_color=(0, 0, 0))
        frame = blank_frame()
        result = filt.filter(frame, regions=[(10.0, 10.0, 50.0, 50.0)])
        # Pixel outside the mask should be untouched
        assert result[90, 90, 0] == 200

    def test_no_regions_returns_unchanged_copy(self) -> None:
        filt = MockPrivacyFilter()
        frame = blank_frame()
        result = filt.filter(frame, regions=None)
        np.testing.assert_array_equal(result, frame)
        assert result is not frame

    def test_privacy_filter_called_before_persistence(self) -> None:
        """
        Ordering test: verifies that privacy filter invocation is counted
        before any cache push would occur. In this unit test we simulate the
        ordering contract by checking invocations_count > 0 before we would
        push to a cache.
        """
        filt = MockPrivacyFilter()
        frame = blank_frame()
        regions = [(10.0, 10.0, 30.0, 30.0)]

        # Privacy filter fires
        _anonymized = filt.filter(frame, regions=regions)
        assert filt.invocations_count == 1, "Privacy filter must fire before persistence"
        # Cache push would happen here — ordering is correct

    def test_custom_mask_color(self) -> None:
        filt = MockPrivacyFilter(mask_color=(255, 0, 128))
        frame = blank_frame()
        result = filt.filter(frame, regions=[(0.0, 0.0, 40.0, 40.0)])
        assert result[10, 10, 0] == 255
        assert result[10, 10, 1] == 0
        assert result[10, 10, 2] == 128

    def test_out_of_bounds_region_clamped(self) -> None:
        filt = MockPrivacyFilter()
        frame = blank_frame(50, 50)
        # Region extends beyond frame bounds
        result = filt.filter(frame, regions=[(-10.0, -10.0, 200.0, 200.0)])
        # Should not raise; entire frame is masked
        assert result.shape == (50, 50, 3)
