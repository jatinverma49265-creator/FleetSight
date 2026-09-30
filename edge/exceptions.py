"""
FleetSight Edge Pipeline Exceptions.

Custom error hierarchy for video ingestion, frame sampling, tracking,
privacy filters, local caching, and store-and-forward synchronization.
"""

from __future__ import annotations


class EdgeError(Exception):
    """Base exception for all edge processing pipeline errors."""


class VideoSourceError(EdgeError):
    """Raised when opening, reading, or configuring a video source fails."""


class VideoSourceNotFoundError(VideoSourceError):
    """Raised when a specified local video file does not exist."""


class RTSPConnectionError(VideoSourceError):
    """Raised when connecting to an RTSP camera stream fails or times out."""


class FrameSamplingError(EdgeError):
    """Raised when sampling parameters (FPS, intervals) are invalid."""


class TrackingError(EdgeError):
    """Raised when tracker associations or state updates fail."""


class PrivacyFilterError(EdgeError):
    """Raised when edge privacy anonymization or frame obfuscation fails."""


class CacheError(EdgeError):
    """Raised when local SQLite event persistence or retrieval fails."""


class SyncTransportError(EdgeError):
    """Raised during store-and-forward dispatch to backend ingestion."""
