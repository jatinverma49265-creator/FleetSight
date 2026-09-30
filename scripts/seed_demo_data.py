"""
Seed script: Populate realistic simulated data for the Jaipur pilot corridor.

Corridors covered:
- MI Road (Ajmeri Gate to Paanch Batti)
- Tonk Road (Rambagh Circle to Gandhi Nagar)
- JLN Marg (Birla Mandir to World Trade Park)
- Civil Lines / Ajmer Road

Buses: RJ14-01, RJ14-07, RJ14-12
All records are explicitly labelled with DataOrigin.SIMULATED.
"""

from __future__ import annotations

import random
from datetime import UTC, datetime, timedelta

from backend.analytics.store import store
from backend.schemas import (
    BoundingBox,
    DataOrigin,
    DetectionClass,
    DetectionEvent,
    DetectionType,
    SeverityLevel,
)


def seed_jaipur_demo_data() -> None:
    """Populate store with realistic multi-bus events."""
    now = datetime.now(UTC)

    # 1. MI Road Deep Pothole (Multi-bus corroborated: RJ14-01, RJ14-07)
    pothole_lat, pothole_lon = 26.9172, 75.8125
    store.ingest_event(
        DetectionEvent(
            type=DetectionType.ROAD_DAMAGE,
            detection_class=DetectionClass.POTHOLE,
            confidence=0.91,
            severity=SeverityLevel.HIGH,
            latitude=pothole_lat,
            longitude=pothole_lon,
            timestamp=now - timedelta(minutes=42),
            camera_id="CAM-FRONT-01",
            bus_id="RJ14-01",
            model_version="yolo11-v0.1.0",
            bbox=BoundingBox(x=0.45, y=0.62, w=0.18, h=0.12),
            data_origin=DataOrigin.SIMULATED,
            evidence_uri="https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80",
        )
    )
    # Pass 2 by RJ14-07 at the same location (slight GPS jitter: ~12m)
    store.ingest_event(
        DetectionEvent(
            type=DetectionType.ROAD_DAMAGE,
            detection_class=DetectionClass.POTHOLE,
            confidence=0.88,
            severity=SeverityLevel.HIGH,
            latitude=pothole_lat + 0.00008,
            longitude=pothole_lon - 0.00005,
            timestamp=now - timedelta(minutes=18),
            camera_id="CAM-FRONT-07",
            bus_id="RJ14-07",
            model_version="yolo11-v0.1.0",
            bbox=BoundingBox(x=0.42, y=0.60, w=0.20, h=0.14),
            data_origin=DataOrigin.SIMULATED,
            evidence_uri="https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80",
        )
    )

    # 2. Tonk Road Major Alligator Crack (Corroborated: RJ14-01, RJ14-12)
    crack_lat, crack_lon = 26.8910, 75.8075
    store.ingest_event(
        DetectionEvent(
            type=DetectionType.ROAD_DAMAGE,
            detection_class=DetectionClass.ALLIGATOR_CRACK,
            confidence=0.86,
            severity=SeverityLevel.HIGH,
            latitude=crack_lat,
            longitude=crack_lon,
            timestamp=now - timedelta(minutes=55),
            camera_id="CAM-FRONT-01",
            bus_id="RJ14-01",
            model_version="yolo11-v0.1.0",
            bbox=BoundingBox(x=0.35, y=0.55, w=0.30, h=0.20),
            data_origin=DataOrigin.SIMULATED,
        )
    )
    store.ingest_event(
        DetectionEvent(
            type=DetectionType.ROAD_DAMAGE,
            detection_class=DetectionClass.ALLIGATOR_CRACK,
            confidence=0.89,
            severity=SeverityLevel.HIGH,
            latitude=crack_lat - 0.00006,
            longitude=crack_lon + 0.00004,
            timestamp=now - timedelta(minutes=24),
            camera_id="CAM-FRONT-12",
            bus_id="RJ14-12",
            model_version="yolo11-v0.1.0",
            bbox=BoundingBox(x=0.38, y=0.58, w=0.28, h=0.18),
            data_origin=DataOrigin.SIMULATED,
        )
    )

    # 3. JLN Marg Waterlogging (Corroborated: RJ14-07, RJ14-12)
    water_lat, water_lon = 26.8850, 75.8150
    store.ingest_event(
        DetectionEvent(
            type=DetectionType.ROAD_DAMAGE,
            detection_class=DetectionClass.WATERLOGGING,
            confidence=0.94,
            severity=SeverityLevel.CRITICAL,
            latitude=water_lat,
            longitude=water_lon,
            timestamp=now - timedelta(minutes=35),
            camera_id="CAM-FRONT-07",
            bus_id="RJ14-07",
            model_version="yolo11-v0.1.0",
            bbox=BoundingBox(x=0.25, y=0.50, w=0.50, h=0.30),
            data_origin=DataOrigin.SIMULATED,
        )
    )
    store.ingest_event(
        DetectionEvent(
            type=DetectionType.ROAD_DAMAGE,
            detection_class=DetectionClass.WATERLOGGING,
            confidence=0.92,
            severity=SeverityLevel.CRITICAL,
            latitude=water_lat + 0.00005,
            longitude=water_lon + 0.00007,
            timestamp=now - timedelta(minutes=10),
            camera_id="CAM-FRONT-12",
            bus_id="RJ14-12",
            model_version="yolo11-v0.1.0",
            bbox=BoundingBox(x=0.22, y=0.52, w=0.52, h=0.28),
            data_origin=DataOrigin.SIMULATED,
        )
    )

    # 4. Civil Lines Damaged Divider (Candidate: Single bus RJ14-12)
    store.ingest_event(
        DetectionEvent(
            type=DetectionType.INFRASTRUCTURE,
            detection_class=DetectionClass.DAMAGED_BARRIER,
            confidence=0.84,
            severity=SeverityLevel.MEDIUM,
            latitude=26.9080,
            longitude=75.7830,
            timestamp=now - timedelta(minutes=14),
            camera_id="CAM-FRONT-12",
            bus_id="RJ14-12",
            model_version="yolo11-v0.1.0",
            bbox=BoundingBox(x=0.10, y=0.45, w=0.15, h=0.25),
            data_origin=DataOrigin.SIMULATED,
        )
    )

    # 5. Paanch Batti Damaged Signboard (Candidate: Single bus RJ14-01)
    store.ingest_event(
        DetectionEvent(
            type=DetectionType.INFRASTRUCTURE,
            detection_class=DetectionClass.DAMAGED_SIGN,
            confidence=0.81,
            severity=SeverityLevel.MEDIUM,
            latitude=26.9150,
            longitude=75.8080,
            timestamp=now - timedelta(minutes=8),
            camera_id="CAM-FRONT-01",
            bus_id="RJ14-01",
            model_version="yolo11-v0.1.0",
            bbox=BoundingBox(x=0.70, y=0.20, w=0.15, h=0.30),
            data_origin=DataOrigin.SIMULATED,
        )
    )

    # 6. Tonk Road Transverse Crack (Candidate: Single bus RJ14-07)
    store.ingest_event(
        DetectionEvent(
            type=DetectionType.ROAD_DAMAGE,
            detection_class=DetectionClass.TRANSVERSE_CRACK,
            confidence=0.79,
            severity=SeverityLevel.LOW,
            latitude=26.8720,
            longitude=75.8020,
            timestamp=now - timedelta(minutes=6),
            camera_id="CAM-FRONT-07",
            bus_id="RJ14-07",
            model_version="yolo11-v0.1.0",
            bbox=BoundingBox(x=0.40, y=0.70, w=0.25, h=0.10),
            data_origin=DataOrigin.SIMULATED,
        )
    )

    # 7. Seed Traffic Events
    traffic_classes = [
        DetectionClass.CAR,
        DetectionClass.TWO_WHEELER,
        DetectionClass.BUS,
        DetectionClass.AUTO_RICKSHAW,
        DetectionClass.TRUCK,
    ]
    corridor_centers = [
        (26.9180, 75.8180),
        (26.8920, 75.8080),
        (26.8925, 75.8175),
    ]

    for _ in range(40):
        c_lat, c_lon = random.choice(corridor_centers)
        store.ingest_event(
            DetectionEvent(
                type=DetectionType.TRAFFIC,
                detection_class=random.choice(traffic_classes),
                confidence=round(random.uniform(0.75, 0.96), 2),
                latitude=c_lat + random.uniform(-0.003, 0.003),
                longitude=c_lon + random.uniform(-0.003, 0.003),
                timestamp=now - timedelta(minutes=random.randint(1, 15)),
                camera_id="CAM-FRONT-01",
                bus_id="RJ14-01",
                model_version="yolo11-v0.1.0",
                data_origin=DataOrigin.SIMULATED,
            )
        )


if __name__ == "__main__":
    seed_jaipur_demo_data()
    print("Seeded Jaipur corridor demo data successfully.")
    print(f"Total issues: {len(store.issues)}")
    print(f"Total work orders: {len(store.work_orders)}")
    print(f"Total audit logs: {len(store.audit_logs)}")
