"""
FleetSight Edge Processing Package.

Edge video ingestion, frame downsampling, inference orchestration,
cross-frame tracking, event deduplication, privacy filtering,
offline SQLite caching, and store-and-forward sync.
"""

from __future__ import annotations

from edge.cache import EventStatus, SQLiteEventCache
from edge.deduplication import DeduplicationConfig, SpatialTemporalDeduplicator
from edge.event_builder import DefaultEventBuilder, EdgeDetectionEvent
from edge.exceptions import (
    CacheError,
    EdgeError,
    FrameSamplingError,
    PrivacyFilterError,
    RTSPConnectionError,
    SyncTransportError,
    TrackingError,
    VideoSourceError,
    VideoSourceNotFoundError,
)
from edge.gps import SimulatedRouteGPSAdapter, StaticGPSAdapter, UnavailableGPSAdapter
from edge.interfaces import (
    EventBuilder,
    EventCache,
    GPSAdapter,
    GPSReading,
    InferenceAdapter,
    PrivacyFilter,
    SyncTransport,
    TrackedDetection,
    TrackerAdapter,
    VideoSource,
)
from edge.orchestrator import EdgePipelineOrchestrator
from edge.privacy import MockPrivacyFilter, NoOpPrivacyFilter
from edge.sampling import FrameSampler, SampledFrame, SamplingConfig
from edge.sources import FileVideoSource, RTSPVideoSource, SimulatedVideoSource
from edge.sync import MockSyncTransport, StoreAndForwardManager
from edge.telemetry import PipelineTelemetry
from edge.tracking import CentroidTracker, TrackerConfig

__all__ = [
    "CacheError",
    "CentroidTracker",
    "DeduplicationConfig",
    "DefaultEventBuilder",
    "EdgeDetectionEvent",
    "EdgeError",
    "EdgePipelineOrchestrator",
    "EventBuilder",
    "EventCache",
    "EventStatus",
    "FileVideoSource",
    "FrameSampler",
    "FrameSamplingError",
    "GPSAdapter",
    "GPSReading",
    "InferenceAdapter",
    "MockPrivacyFilter",
    "MockSyncTransport",
    "NoOpPrivacyFilter",
    "PipelineTelemetry",
    "PrivacyFilter",
    "PrivacyFilterError",
    "RTSPConnectionError",
    "RTSPVideoSource",
    "SQLiteEventCache",
    "SampledFrame",
    "SamplingConfig",
    "SimulatedRouteGPSAdapter",
    "SimulatedVideoSource",
    "SpatialTemporalDeduplicator",
    "StaticGPSAdapter",
    "StoreAndForwardManager",
    "SyncTransport",
    "SyncTransportError",
    "TrackedDetection",
    "TrackerAdapter",
    "TrackerConfig",
    "TrackingError",
    "UnavailableGPSAdapter",
    "VideoSource",
    "VideoSourceError",
    "VideoSourceNotFoundError",
]
