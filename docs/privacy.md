# FleetSight — Privacy & Data Protection Architecture

> **Document Status**: PRIVACY & COMPLIANCE FRAMEWORK (LOOP 1 FOUNDATION)  
> **Applicable Regulations**: Digital Personal Data Protection (DPDP) Act, 2023 (India) & Global Privacy Best Practices

---

## 1. Privacy-by-Design Philosophy

Public transport buses traverse public thoroughfares, inherently recording pedestrian faces, residential structures, and private vehicle license plates. FleetSight is architected from day one under the doctrine of **Privacy-by-Design and Default**:
1. Raw dashcam footage does **NOT** leave the local bus edge compute node in unredacted form.
2. The central platform collects **distress events and spatial metadata**, not full-resolution surveillance video streams.

---

## 2. Edge Anonymization Layer

Before any crop, thumbnail, or evidentiary frame is persisted to the local cache (`EventCache`) or uploaded to the FleetSight ingestion endpoint:
- **Face Blurring**:
  - Activated by default (`PRIVACY_BLUR_FACES=true`).
  - Edge lightweight face detection applies Gaussian blur / pixelation across all detected facial bounding boxes.
- **License Plate Blurring**:
  - Activated by default (`PRIVACY_BLUR_PLATES=true`).
  - Vehicle registration plates are blurred at the edge prior to evidence storage.
- **Explicit Prohibition on ANPR in Early Loops**:
  - Automated Number Plate Recognition (ANPR) and identity profiling are **strictly out of scope** and prohibited in the edge pipeline to prevent privacy erosion and mission creep.

---

## 3. Evidence Access Control & Storage Security

When visual evidence is attached to a detection event (e.g. road distress verification):
- **Object Storage Access**: Evidence frames are referenced via `evidence_uri`. These URIs are not public; they are protected by time-limited signed URLs or scoped IAM credentials.
- **Access Authorization**: Inspection of full-resolution evidence crops is restricted to authorized municipal engineers and vetted auditing personnel.
- **Retention & Ephemeral Edge Storage**: Edge video rings buffer only transiently in RAM or local temporary block storage; non-detection frames are purged on a rolling FIFO basis.

---

## 4. Auditability & Data Minimization

- **Minimal Metadata**: Events transmit only necessary telemetry: GPS coordinates, timestamp, camera/bus identifiers, detection class, confidence, and bounded crops.
- **Audit Logs**: All access to evidence images, work-order status modifications, and data exports are recorded in append-only audit logs.
- **Zero Secrets in Repository**: Secrets, credentials, and API keys are strictly forbidden from version control and verified via automated linting and pre-commit checks.
