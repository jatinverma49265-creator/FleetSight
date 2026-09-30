# FleetSight — Architecture & System Design

> **Document Status**: ARCHITECTURE SPECIFICATION (LOOP 1 FOUNDATION)  
> **Claim Status**: TARGET ARCHITECTURE (NOT MEASURED PRODUCTION METRICS)

---

## 1. System Overview

FleetSight transforms public transport buses into mobile urban intelligence sensing units. By mounting forward-facing camera sensors and telemetry units (GPS/IMU) on scheduled municipal bus routes, the system continuously monitors road surfaces, roadside assets, and traffic conditions across an entire city without requiring dedicated inspection fleets.

---

## 2. End-to-End Pipeline

```
+--------------------------------------------------------------------+
|                             ON-BUS EDGE                            |
+--------------------------------------------------------------------+
|  Bus Dashcam / Video Input (RTSP / USB / Local File)               |
|                               |                                    |
|                               v                                    |
|  Edge AI Inference (Detector Protocol: YOLO11 / YOLO12 / YOLO26)   |
|                               |                                    |
|                               v                                    |
|  Tracking & Deduplication (TrackerAdapter: ByteTrack / BoT-SORT)    |
|                               |                                    |
|                               v                                    |
|  Privacy Layer (Face & License Plate Blurring by Default)          |
|                               |                                    |
|                               v                                    |
|  Event Builder (Attaches GPS, Timestamp, Bus ID, Camera ID)        |
|                               |                                    |
|                               v                                    |
|  Local SQLite / JSONL Event Cache (Handles Offline Connectivity)    |
+--------------------------------------------------------------------+
                                | (HTTP / MQTT / Cellular Sync)
                                v
+--------------------------------------------------------------------+
|                           CENTRAL BACKEND                          |
+--------------------------------------------------------------------+
|  FastAPI Event Ingestion API (/api/v1/events)                      |
|                               |                                    |
|                               v                                    |
|  PostgreSQL + PostGIS Database (Spatial Indexing)                  |
|                               |                                    |
|                               v                                    |
|  Clustering & Spatial Corroboration Engine                         |
|  (Cross-validates detections from multiple buses & passes)          |
|                               |                                    |
|                               v                                    |
|  Severity & Priority Assessment Engine                             |
|  (Formulaic, transparent calculation based on size, recurrence)    |
|                               |                                    |
|                               v                                    |
|  Work-Order Candidate Generation & Audit Logging                   |
+--------------------------------------------------------------------+
                                |
                                v
+--------------------------------------------------------------------+
|                             FRONTEND                               |
+--------------------------------------------------------------------+
|  GIS Dashboard (MapLibre / Leaflet + React / Vite)                 |
|  (Layered visualization of road damage, traffic, infrastructure)   |
+--------------------------------------------------------------------+
```

---

## 3. Core Architectural Principles

1. **Decoupled Edge and Cloud**:
   - The edge pipeline operates fully offline when cellular connectivity is unavailable. Events are persisted to an atomic local cache (`EventCache`) and synced opportunistically.
2. **Model Backend Agnosticism**:
   - Inference is accessed strictly through the `Detector` protocol (`ml/detector.py`). The application code never directly binds to a single YOLO vendor or version.
3. **Strict Data Contracts**:
   - All events conform to the versioned `DetectionEvent` schema (`backend/schemas.py`). Events require explicit provenance tagging (`MEASURED`, `SIMULATED`, or `ILLUSTRATIVE`).
4. **Privacy-by-Design**:
   - Face and license plate obfuscation is performed at the edge before raw frames or crop evidence are cached or transmitted.
5. **No Premature Complexity**:
   - Database persistence, ML fine-tuning, complex agent workflows, and GIS UI are introduced in staged loops with explicit validation.
