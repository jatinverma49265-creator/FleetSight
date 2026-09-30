# FleetSight — Privacy Policy & Data Protection Charter

> **Version**: 1.0.0  
> **Effective Date**: September 30, 2026  
> **Regulatory Alignment**: Digital Personal Data Protection (DPDP) Act, 2023 (India)  
> **Classification**: Public / Civic Infrastructure

---

## 1. Executive Summary & Purpose

FleetSight is an automated road infrastructure monitoring and mobile urban sensing platform. By mounting low-power edge vision devices on existing public transit buses, FleetSight identifies road hazards (potholes, severe cracks, damaged signage, waterlogging) to assist municipal corporations and public works departments (PWD) in maintaining safer roads.

**Core Privacy Commitment**: FleetSight is designed from the silicon layer up to monitor **road infrastructure**, not individuals. We do not conduct surveillance, identify citizens, or store identifiable personal data.

---

## 2. DPDP Act 2023 Alignment Principles

| DPDP Act 2023 Principle | FleetSight Technical Implementation |
| :--- | :--- |
| **Notice & Transparency (Sec. 5)** | Public notices on transit buses and publicly accessible web portal detailing sensing scope and objectives. |
| **Purpose Limitation (Sec. 6)** | Data processing is strictly confined to detecting physical roadway defects and computing aggregate corridor traffic flow. |
| **Data Minimisation (Sec. 6(1))** | Raw video is processed in volatile RAM at the edge and never streamed to the cloud. Only compact, anonymized bounding box coordinates and GPS telemetry are transmitted. |
| **Edge De-Identification & Redaction** | Any accidental capture of human faces or motor vehicle registration plates is permanently blurred using Gaussian filters *on the edge device* before image persistence. |
| **No ANPR / No Facial Recognition** | Automatic Number Plate Recognition (ANPR) and facial recognition modules are explicitly excluded and prohibited from the codebase. |
| **Storage Limitation (Sec. 8(7))** | Telemetry logs and aggregate traffic indices are retained only for analytical validity (maximum 90 days), after which records are automatically purged or aggregated. |
| **Security Safeguards (Sec. 8(5))** | TLS 1.3 encryption in transit, role-based access control (RBAC), and append-only immutable audit logging for all mutations. |

---

## 3. What Data We Process vs What We Never Collect

### Data Processed
1. **Physical Road Defect Metadata**: Type (pothole, crack, damaged sign), bounding box coordinates, estimated severity score (0–100), and GPS coordinates.
2. **Transit Vehicle Telemetry**: Bus identifier, anonymous route number, GPS speed, and sensor timestamp.
3. **Aggregate Traffic Density**: Anonymized vehicle counts per 15-minute window for corridor maintenance scheduling.

### Data We NEVER Collect or Store
- ❌ Human Facial Embeddings or Biometrics
- ❌ Motor Vehicle License Plate Numbers (No ANPR)
- ❌ Pedestrian Trajectories or Tracking
- ❌ Passenger In-Cabin Video or Audio
- ❌ Continuous High-Definition Video Feeds

---

## 4. Edge-First Privacy Pipeline

```
[ Camera Sensor ]
        │ (1080p / 720p raw frames in RAM)
        ▼
[ Edge AI Inference ] (YOLO Defect & Object Detection)
        │
        ▼
[ Privacy Redaction Layer ] ──> Gaussian Blur / Mask on all detected faces & plates
        │
        ▼
[ Telemetry JSON Extraction ] ──> ~320 bytes payload (GPS + bbox + defect type)
        │
        ▼ (Raw video frame discarded from RAM immediately)
[ HTTPS Ingest Pipeline ] ──> Central Command Center
```

---

## 5. Contact & Data Protection Officer (DPO)

For inquiries or compliance verifications regarding municipal deployments:
- **DPO Desk**: `dpo@fleetsight.gov.in` (Simulated Prototype Desk)
- **Authority**: Municipal Corporation of Greater Jaipur / Smart City Mission Pilot
- **Prototype Disclaimer**: This deployment is currently operating under the **Smart India Hackathon 2026** research sandbox with simulated and synthetic datasets (`data_origin="simulated"`).
