# FleetSight — Development Guide & Workflow

> **Document Status**: DEVELOPER RUNBOOK (LOOP 1 + LOOP 2 FOUNDATION)

---

## 1. Prerequisites

- **Python**: 3.11 or higher
- **Virtual Environment**: `.venv`
- **Docker & Docker Compose**: Optional for local PostgreSQL/PostGIS database execution

---

## 2. Local Environment Setup

1. **Clone & Navigate**:
   ```bash
   cd FleetSight
   ```

2. **Initialize Python Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate Environment**:
   - Windows PowerShell:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies in Editable Mode**:
   ```bash
   pip install -e ".[dev,ml]"
   ```

5. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

---

## 3. Running the Backend

Start the FastAPI application with auto-reload:

```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

---

## 4. Running the Test Suite & Quality Gates

Execute pytest across all unit, API integration, and ML foundation tests:

```bash
pytest -v
```

Execute code formatting and linting:

```bash
ruff check .
```

Execute static type checking:

```bash
mypy backend edge ml tests
```

---

## 5. Development Infrastructure (Docker Compose)

To spin up the development PostgreSQL + PostGIS database:

```bash
docker compose up -d db
```

To stop the containers:

```bash
docker compose down
```

---

## 6. Monorepo Structure

```
FleetSight/
├── backend/                  # FastAPI application, configuration, data contracts, API routes
│   ├── api/v1/               # Versioned API routes (events, health)
│   ├── app.py                # ASGI application factory
│   ├── config.py             # Pydantic Settings environment configuration
│   ├── logging_config.py     # Structured logging setup
│   └── schemas.py            # Canonical Pydantic event contracts
├── edge/                     # On-bus edge processing pipeline abstractions
│   └── interfaces.py         # Protocols: VideoSource, InferenceAdapter, TrackerAdapter, GPS, Cache
├── ml/                       # Machine Learning & dataset pipeline foundation
│   ├── config/               # Pydantic configuration schemas (train, eval, inference, benchmark)
│   ├── datasets/             # Manifests, RDD2022/COCO/Jaipur definitions, splitters, validators
│   │   ├── manifests/        # Machine-readable dataset_manifest.yaml
│   │   ├── coco.py           # COCO 80-class mapping
│   │   ├── exceptions.py     # Structured ML/Dataset exceptions (missing data, license checks)
│   │   ├── jaipur.py         # Jaipur local dataset structure (200-500 frames) & telemetry metadata
│   │   ├── manifest.py       # DatasetManifest, DatasetType, DatasetStatus, load_default_manifest
│   │   ├── rdd2022.py        # RDD2022 CRDDC class taxonomy converter
│   │   ├── split.py          # Route- and day-aware anti-leakage splitting engine
│   │   └── validator.py      # YOLO annotation validator & dataset consistency checker
│   ├── detector.py           # Detector protocol & detection dataclasses
│   ├── metrics.py            # Typed metrics (8 targets) & BenchmarkReport container
│   ├── models/               # Concrete detector adapters
│   │   ├── base.py           # BaseYOLOAdapter with safe missing-weights handling
│   │   ├── yolo11.py         # YOLO11 baseline candidate adapter
│   │   ├── yolo12.py         # YOLO12 experimental candidate adapter
│   │   └── yolo26.py         # YOLO26 speculative candidate adapter
│   └── registry.py           # Factory registry for model backends
├── docs/                     # Architecture, data strategy, ML strategy, privacy, development
├── infra/                    # Dockerfiles, deployment manifests
├── tests/                    # Pytest test suite (health, schemas, API, ML datasets, models, metrics)
├── data/                     # Offline dataset hierarchy (raw, processed, annotations, manifests, splits, local)
├── pyproject.toml            # Python project manifest and dependency definitions
├── docker-compose.yml        # Local multi-container development orchestration
├── .env.example              # Environment variable template
└── README.md                 # Repository overview
```
