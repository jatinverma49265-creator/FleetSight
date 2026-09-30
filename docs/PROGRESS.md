# FleetSight — Development Progress & Master Tracking

> **Single Source of Truth** for FleetSight prototype development across Loops 1 to 11 (Smart India Hackathon 2026 · PS SIH26124).  
> **Last Updated**: 2026-09-30  
> **Repository**: `FleetSight` (Edge AI on public-bus cameras -> compact GPS events -> FastAPI backend -> clustering & 2+ bus corroboration -> severity ranking -> GIS command center & public portal)

---

## 1. Loop Status Overview

| Loop | Title | Status | Date | Key Deliverables & Highlights |
| :--- | :--- | :--- | :--- | :--- |
| **Loop 1** | Audit & Workspace Foundation | ✅ Complete | 2026-09-30 | pyproject.toml, architecture, data/ML/privacy strategy docs, project structure. |
| **Loop 2A** | Dataset Foundation | ✅ Complete | 2026-09-30 | RDD2022 / Jaipur dataset adapters, COCO/YOLO annotation validators, split manager, class mappings. |
| **Loop 2B** | Model Abstraction & Benchmark | ✅ Complete | 2026-09-30 | `Detector` protocol, YOLO11/12/26 model adapters, registry, mAP@0.5 evaluation metrics. |
| **Loop 2C** | Edge Inference Pipeline | ✅ Complete | 2026-09-30 | Video sources (RTSP, File, Synthetic), adaptive frame sampling, ByteTrack/BoT-SORT tracker adapters. |
| **Loop 3** | Edge Event Generation & Privacy | ✅ Complete | 2026-09-30 | Privacy blur engine (faces/plates), single-bus deduplication, GPS/telemetry attach, local SQLite cache & sync orchestrator. |
| **Loop 4** | FastAPI Backend & Persistence | ✅ Complete | 2026-09-30 | FastAPI app, data contracts (`DetectionEvent`), `/api/v1/events` ingestion, in-memory store, `/api/v1/kpis`. |
| **Loop 5** | Verification, Corroboration & Severity | ✅ Complete | 2026-09-30 | Spatial clustering (<=35m), 2+ bus corroboration promoting candidates to verified, explainable severity breakdown scoring (0-100), work-order state machine with RBAC. |
| **Loop 6** | GIS Dashboard (Command Center) | ✅ Complete | 2026-09-30 | React + Vite + Leaflet + Recharts GIS Command Center. Interactive Jaipur corridor map, traffic heat layer, explainable work order queue, role-based views (Admin, Engineer, Police, Viewer), live audit trail, 5s polling, and verified screenshots. |
| **Loop 7** | Simulated 2-3 Bus Demo | ⏳ Next | Pending | Deterministic Jaipur corridor replay (`scripts/simulate_buses.py`), offline store-and-forward re-sync test, re-detection closure/escalation loop. |
| **Loop 8** | End-to-End Testing & Performance | ⏳ Planned | Pending | Pytest E2E + Playwright suites, automatic latency/bandwidth/accuracy benchmark scripts generating `docs/metrics.md`. |
| **Loop 9** | Public Website, Privacy & Legal | ⏳ Planned | Pending | Public portal (problem, sourced statistics, architecture, bus sensing loop, DPDP Act 2023 privacy policy, WCAG 2.1 AA accessibility, disclaimer). |
| **Loop 10** | Final Demo & Documentation | ⏳ Planned | Pending | Comprehensive README, architecture diagrams, `docs/demo.md` (6-min script), `docs/qa.md`, fresh-clone verification. |
| **Loop 11** | Public Release (Locked) | 🔒 Locked | Pending | Secret scan (gitleaks), licence compliance (MIT/Apache + YOLO AGPL/RDD notice), repo hygiene, release readiness. |

---

## 2. Component Inventory & Audit

### Edge & ML Subsystems (Loops 2A, 2B, 2C, 3)
- **ML Datasets & Splits**: `ml/datasets/` (validation, COCO/RDD2022 formats, leak-free route/time splits).
- **ML Models & Detectors**: `ml/models/` (YOLO11, YOLO12, YOLO26 abstractions), `ml/registry.py`, `ml/metrics.py`.
- **Edge Inference & Sampling**: `edge/sources/` (RTSP, file, synthetic), `edge/sampling.py` (speed-adaptive 2–15 FPS), `edge/tracking.py` (IoU + velocity tracker).
- **Edge Privacy & Deduplication**: `edge/privacy.py` (Gaussian face blur, plate masking), `edge/deduplication.py` (spatial-temporal single-bus window).
- **Edge Cache & Sync**: `edge/cache.py` (atomic SQLite cache), `edge/sync.py` (HTTP store-and-forward with exponential backoff), `edge/orchestrator.py`.

### Backend & Analytics Subsystems (Loops 4, 5)
- **FastAPI Core**: `backend/app.py`, `backend/config.py`, `backend/logging_config.py`.
- **Data Contracts**: `backend/schemas.py` (`DetectionEvent`, `BoundingBox`, `DetectionClass`, `DataOrigin`, `SeverityLevel`).
- **Endpoints Active**:
  - `GET /health`
  - `POST /api/v1/events/` (ingestion with provenance validation)
  - `GET /api/v1/events/` (recent event stream)
- **Endpoints Being Extended for Loop 5/6**:
  - `GET /api/v1/issues` (clustered spatial issues with status filtering: candidate, verified, work_order, repaired)
  - `GET /api/v1/work-orders` & `PATCH /api/v1/work-orders/{id}` (ranked queue with explainable severity breakdown and RBAC state transitions)
  - `GET /api/v1/traffic` (15-minute corridor segment vehicle heat counts)
  - `GET /api/v1/kpis` (fleet and defect operational statistics)
  - `GET /api/v1/audit` (immutable access/mutation log for admin/police)
  - `POST /api/v1/auth/login` (RBAC session/token with roles: `admin`, `engineer`, `police`, `viewer`)

---

## 3. Provenance & Truth in Labeling
- All synthetic / simulated data records include `data_origin: "simulated"` and UI badges with `SIMULATED DATA · PROTOTYPE`.
- MoRTH 2022 sourced stats: 4,61,312 road accidents, 1,68,491 fatalities; pedestrian deaths 29,124 to 32,825; Delhi 7,678 potholes identified, 4,003 repaired.
- Target prototype metrics clearly distinguished from measured runtime benchmarks (measured in Loop 8).

---

## 4. Known Issues & Resolved Items
1. **Resolved**: Python 3.14 / pytest starlette deprecation filter resolved in `pyproject.toml`; full test suite passing (145/145 unit & integration tests).
2. **Resolved**: Package installed in editable mode (`pip install -e .[dev,ml,db]`) with all core dependencies.
3. **Pending Loop 6**: Complete GIS Dashboard with interactive Leaflet map, corridor traffic heat layer, RBAC views, live polling, and explainable work orders.
