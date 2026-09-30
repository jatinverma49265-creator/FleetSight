"""
GPS Provider Adapters.

Provides interfaces and reference adapters for on-bus GPS telemetry ingestion.
Supports simulated GPS trajectories for testing and explicit null states when hardware is offline.
Never fabricates real-world coordinates unless explicitly configured as simulation.
"""

from __future__ import annotations

from datetime import UTC, datetime

from edge.interfaces import GPSAdapter, GPSReading


class UnavailableGPSAdapter(GPSAdapter):
    """Represents an edge device with no active GPS receiver or lost satellite lock."""

    def latest(self) -> GPSReading | None:
        """Explicitly return None to represent missing geolocation telemetry."""
        return None


class StaticGPSAdapter(GPSAdapter):
    """Provides a fixed, known GPS fix (e.g. for testing depot/stop geofencing)."""

    def __init__(
        self,
        latitude: float,
        longitude: float,
        speed_kmh: float = 0.0,
        is_simulated: bool = False,
    ) -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.speed_kmh = speed_kmh
        self.is_simulated = is_simulated

    def latest(self) -> GPSReading | None:
        return GPSReading(
            latitude=self.latitude,
            longitude=self.longitude,
            speed_kmh=self.speed_kmh,
            timestamp=datetime.now(UTC),
        )


class SimulatedRouteGPSAdapter(GPSAdapter):
    """
    Interpolates coordinates along a simulated route corridor for integration tests.

    Explicitly tagged as simulated telemetry.
    """

    def __init__(
        self,
        start_lat: float = 26.9124,
        start_lon: float = 75.7873,
        step_lat: float = 0.0001,
        step_lon: float = 0.0001,
        speed_kmh: float = 30.0,
    ) -> None:
        self.current_lat = start_lat
        self.current_lon = start_lon
        self.step_lat = step_lat
        self.step_lon = step_lon
        self.speed_kmh = speed_kmh
        self.is_simulated = True

    def latest(self) -> GPSReading | None:
        reading = GPSReading(
            latitude=round(self.current_lat, 6),
            longitude=round(self.current_lon, 6),
            speed_kmh=self.speed_kmh,
            timestamp=datetime.now(UTC),
        )
        # Advance along trajectory
        self.current_lat += self.step_lat
        self.current_lon += self.step_lon
        return reading
