# FleetSight — Autonomous Urban Sensing & Infrastructure Intelligence

FleetSight is an edge-AI-powered urban road monitoring prototype that turns everyday public transport buses into mobile road inspection units.

Instead of depending on dedicated survey vehicles, FleetSight is designed to use cameras mounted on buses to identify road defects such as potholes, cracks, waterlogging and damaged road signage as they travel along their regular routes.

The system processes video locally and sends compact detection events to a central GIS dashboard, giving civic teams a way to review, verify and prioritise reported infrastructure issues.

## How it works

1. **Capture:** A camera on a bus provides road footage to the onboard edge device.
2. **Detect and track:** Computer-vision models identify possible road defects, while tracking helps avoid repeatedly reporting the same observation across adjacent frames.
3. **Protect privacy:** Face and number-plate regions are blurred locally. The prototype is designed without facial recognition or automated number-plate recognition.
4. **Queue and sync:** Detection events are stored locally and forwarded when connectivity is available, rather than continuously uploading raw video.
5. **Verify observations:** Reports from multiple buses can be correlated by location to increase confidence in a detected issue.
6. **Review and act:** A GIS dashboard displays issues and supports role-based review and work-order workflows.
7. **Check repairs:** Later bus passes can be used to check whether a previously reported defect is still visible.

## Main capabilities

- YOLO-based road-defect detection
- Multi-frame object tracking
- On-device privacy redaction
- Offline store-and-forward event caching
- Compact event-based reporting for low-bandwidth connections
- Multi-bus spatial corroboration
- Explainable issue-priority scoring
- Interactive GIS dashboard and traffic visualisation
- Role-based access and work-order management
- Re-detection workflow for repair verification

## Technology

| Area | Technologies |
|---|---|
| Backend | Python, FastAPI, Pydantic |
| Frontend | React, Vite |
| Mapping and visualisation | Leaflet, Recharts |
| Computer vision | YOLO-based detection, object tracking |
| Local data and caching | SQLite |
| Testing | Pytest, Playwright |

## Repository structure

```text
FleetSight/
├── backend/       # API, ingestion, analytics and work-order services
├── edge/          # Onboard inference, privacy, tracking, cache and sync
├── frontend/      # React GIS dashboard and public portal
├── docs/          # Architecture, metrics, privacy and demo documentation
├── scripts/       # Simulation and benchmark utilities
└── tests/         # Automated backend and integration tests
```

## Getting started

### Prerequisites

- Python 3.11 or later
- Node.js 18 or later
- npm

### 1. Clone the repository

```bash
git clone https://github.com/jatinverma49265-creator/FleetSight.git
cd FleetSight
```

### 2. Install backend dependencies

```bash
pip install -e .
```

### 3. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Start the backend

From the repository root, run:

```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Start the frontend

In a second terminal:

```bash
cd frontend
npm run dev
```

Open **http://127.0.0.1:5173/** in your browser.

## Run the demo scenarios

Run the end-to-end simulated corridor scenario:

```bash
python scripts/run_demo_scenario.py
```

Run a standalone multi-bus simulation:

```bash
python scripts/simulate_buses.py --buses RJ14-01,RJ14-07,RJ14-12 --interval 0.5
```

Generate benchmark output:

```bash
python scripts/benchmark_and_metrics.py
```

## Run tests

Run the Python test suite from the repository root:

```bash
pytest -v
```

Run the frontend browser tests:

```bash
cd frontend
node test_e2e.js
```

For the latest test coverage, benchmark methodology and measured results, refer to the files in [`docs/`](docs/).

## Privacy and data handling

FleetSight follows a privacy-by-design approach for its prototype workflow. Video frames are processed locally, with face and number-plate redaction applied before event reporting. The intended event pipeline sends structured detection metadata rather than a continuous video feed. Review [`docs/privacy_policy.md`](docs/privacy_policy.md) for the project's privacy documentation.

## Project context

FleetSight was developed as a prototype for **Smart India Hackathon 2026**, under **Problem Statement SIH26124**.

Simulation-generated events are labelled as simulated data. Benchmark results should be read alongside their documented datasets, test conditions and methodology. Performance in live municipal deployments, including real-world false-positive rates, requires validation with field data.

## License

This project is licensed under the [Apache License 2.0](LICENSE).

---

FleetSight explores how existing public transport infrastructure can help cities monitor road conditions more frequently and make infrastructure maintenance more data-informed.
