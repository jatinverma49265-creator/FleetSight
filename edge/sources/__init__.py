"""
FleetSight Edge Video Sources Package.

Concrete implementations for local file capture, simulated dashcam generation,
and RTSP network streaming.
"""

from __future__ import annotations

from edge.sources.file_source import FileVideoSource
from edge.sources.rtsp import RTSPVideoSource
from edge.sources.simulated import SimulatedVideoSource

__all__ = [
    "FileVideoSource",
    "RTSPVideoSource",
    "SimulatedVideoSource",
]
