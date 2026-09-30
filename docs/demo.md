# FleetSight — 6-Minute Pitch & Live Demonstration Script

> **Event**: Smart India Hackathon 2026  
> **Problem Statement**: SIH26124 (Mobile Urban Sensing via Public Transit Buses)  
> **Target Audience**: SIH Jury, Ministry Representatives, Municipal Commissioners, PWD Chief Engineers  
> **Total Duration**: 6 Minutes (360 seconds)

---

## Chronological Demo Rundown

```
[0:00 ─── 1:00]  Problem Context & MoRTH 2022 Data Baseline
[1:00 ─── 2:00]  The FleetSight Core Innovation & Edge Architecture
[2:00 ─── 3:00]  Live Demo: Pass 1 Candidate & GIS Live Map
[3:00 ─── 4:00]  Live Demo: Pass 2 Corroboration & Explainable Scoring
[4:00 ─── 5:00]  PWD Work Order Dispatch & RBAC Security
[5:00 ─── 6:00]  Closed-Loop Re-Detection Verification & Wrap-Up
```

---

### Phase 1: Problem Context & Data Baseline (0:00 – 1:00)
**Screen Display**: Public Portal (`http://127.0.0.1:5173/` - Tab: *Public Portal & DPDP*)

**Presenter Script**:
> "Respected Jury, in 2022, India recorded **4,61,312 road accidents** resulting in **1,68,491 tragic fatalities**—over 32,000 of them pedestrians—as documented by the Ministry of Road Transport and Highways (MoRTH).
> 
> Today, municipal corporations rely on manual citizen complaints or dedicated survey vehicles that cost over ₹50 Lakhs each and survey corridors only once every few months. By the time a pothole is logged, accidents have already occurred.
> 
> We asked a fundamental question: **What if the public buses that already traverse our city streets every single day became real-time mobile road inspectors?**
> 
> Introducing **FleetSight**."

---

### Phase 2: Core Innovation & Edge Architecture (1:00 – 2:00)
**Screen Display**: Public Portal (*5-Stage Closed-Loop & Bandwidth Modal*)

**Presenter Script**:
> "FleetSight places lightweight edge vision devices on municipal transit buses (like JCTSL in Jaipur or DTC in Delhi).
> 
> Here are our core architectural breakthroughs:
> 1. **99.99% Bandwidth Reduction**: Instead of streaming continuous 720p/1080p video (which consumes over 2 GB per hour per bus and chokes cellular bandwidth), our YOLO models run directly on the edge in volatile RAM. We transmit **only compact ~320-byte JSON telemetry events** (saving 100% video bandwidth).
> 2. **DPDP Act 2023 Privacy-by-Design**: Human faces and motor vehicle license plates are permanently blurred *on the camera hardware* before anything is cached. There is **zero facial recognition and zero ANPR**.
> 3. **Store-and-Forward Offline Resilience**: In cellular dead zones, events are buffered in an atomic SQLite cache and synced upon reconnection with **guaranteed zero duplicate records**."

---

### Phase 3: Live Demo — Pass 1 & Single-Bus Candidate (2:00 – 3:00)
**Action**: Click **"Launch GIS Command Center"** $\to$ Click **"▶ Run Pass 1 (Bus RJ14-01)"** in Demo Control Panel.  
**Screen Display**: GIS Live Map (`/map`)

**Presenter Script**:
> "Let's watch this live on our Jaipur pilot corridor from MI Road to Tonk Road.
> 
> Bus `RJ14-01` passes down MI Road and detects a deep pothole. Notice what happens in our GIS Command Center:
> - The defect appears immediately on our interactive Leaflet map.
> - But notice its status: **`CANDIDATE`** with a yellow badge.
> - Why? Because in real cities, a shadow or road reflection can fool a single camera. FleetSight never wastes public funds on single-camera uncorroborated detections."

---

### Phase 4: Live Demo — Pass 2 Corroboration & Explainable Scoring (3:00 – 4:00)
**Action**: Click **"▶ Run Pass 2 (Bus RJ14-07: Corroboration)"**.  
**Screen Display**: Click on the map marker to open the **Detail Drawer**.

**Presenter Script**:
> "Fifteen minutes later, Bus `RJ14-07` surveys the same corridor.
> 
> Instantly, our spatial clustering engine (using a 35-meter Haversine threshold) matches the coordinates. Look at the state transition:
> - The issue is automatically promoted from Candidate to **`VERIFIED`** and enters the **Work Order Queue**!
> - Let's inspect the **Explainable Priority Score Breakdown**:
>   - Base Defect Weight: **35 pts** (Severe Pothole)
>   - ML Detection Confidence: **18 pts** (94% confidence)
>   - Multi-Bus Recurrence Corroboration: **+20 pts** (Confirmed by 2 independent buses)
>   - Corridor Traffic Multiplier: **+15 pts** (High-density public transit arterial)
>   - **Total Priority Score: 88 / 100**.
> 
> Municipal engineers have full mathematical explainability for why this pothole is prioritized first."

---

### Phase 5: PWD Work Order Dispatch & RBAC Security (4:00 – 5:00)
**Action**: 
1. Switch Role Dropdown to **"Public Viewer"** $\to$ Attempt to click **"Approve & Dispatch"** (triggers 403 Denial Modal).
2. Switch Role to **"PWD Engineer"** $\to$ Click **"Approve & Dispatch"** (transitions to `ASSIGNED`).

**Presenter Script**:
> "Now let's look at municipal governance and security.
> 
> Under our Role-Based Access Control (RBAC):
> - If a public citizen or unauthenticated viewer attempts to modify a repair order, the system strictly denies access with a **403 Forbidden modal**.
> - When logged in as **PWD Engineer**, the engineer approves the work order and assigns it to 'Jaipur Municipal Works Div-3'.
> - Every single mutation is immutably logged in our **Audit Trail** for total civic accountability."

---

### Phase 6: Closed-Loop Re-Detection Verification & Conclusion (5:00 – 6:00)
**Action**: Click **"▶ Simulate Repair & Re-detection Pass"** $\to$ Status transitions to **`CLOSED`** with green badge.

**Presenter Script**:
> "Finally, the repair crew patches the road. But how does the city verify the contractor actually did the work without sending another inspector?
> 
> The next morning, Bus `RJ14-12` drives over the same coordinate. Our edge model detects **zero hazards**.
> 
> FleetSight closes the loop: **The work order is automatically proposed for closure and verified repaired!**
> 
> If the pothole had persisted, the system would have escalated the contractor for SLA violation.
> 
> **Summary**:
> - **100% Bandwidth Saved** (1.6 KB JSON vs 2.08 GB video)
> - **2+ Bus Corroboration** for zero false-alarm dispatches
> - **DPDP Act 2023 Privacy Compliance**
> - **Autonomous Re-detection Closed Loop**
> 
> FleetSight is ready to make India's smart cities safer, one bus ride at a time. Thank you!"
