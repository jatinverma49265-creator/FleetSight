# FleetSight — Data Strategy, Provenance & Governance

> **Document Status**: DATA MANAGEMENT & PIPELINE SPECIFICATION (LOOP 2 IMPLEMENTATION)  
> **Claim Status**: TARGET SPECIFICATION & GOVERNANCE PROTOCOL (NO FABRICATED METRICS)

---

## 1. Overview & Data Categories

FleetSight enforces a strict multi-tiered data strategy to prevent data contamination and preserve academic/competition integrity.

| Category | Datasets | Role | License & Compliance |
|---|---|---|---|
| **Public Benchmark** | `rdd2022`, `coco_pretrained` | Baseline road distress & general vehicle/pedestrian detection | CC BY-SA 4.0 (RDD2022 attribution) & CC BY 4.0 (COCO) |
| **Real Local** | `jaipur_custom` (200–500 frames) | Domain adaptation on Jaipur roads, lighting & weather | Municipal pilot authorization, consent verified, face/plate blurred |
| **Optional Restricted** | `idd_india_driving_dataset`, `roboflow_pothole_optional` | Secondary candidate reference for unconstrained Indian traffic | Gated behind programmatic `LicenseVerificationError` |
| **Simulated Demo** | `simulated_demo` | Integration testing, API stress testing, offline mock demo | Synthetic data origin; strictly isolated from benchmarks |

---

## 2. Dataset Provenance and Attribution

All datasets incorporated into FleetSight maintain machine-readable provenance in `ml/datasets/manifests/dataset_manifest.yaml` and programmatic enforcement via `ml.datasets.manifest.DatasetManifest`.

### 2.1 RDD2022 Baseline (Road Damage Detection)
- **Role**: Primary baseline training and evaluation dataset for road distress.
- **Classes targeted**:
  - `D00`: Longitudinal Crack -> mapped to `DetectionClass.LONGITUDINAL_CRACK`
  - `D10`: Transverse Crack -> mapped to `DetectionClass.TRANSVERSE_CRACK`
  - `D20`: Alligator Crack -> mapped to `DetectionClass.ALLIGATOR_CRACK`
  - `D40`: Pothole -> mapped to `DetectionClass.POTHOLE`
- **Provenance**: Crowdsourced Road Damage Detection Challenge (CRDDC 2022, Sekilab).
- **Mandatory Attribution**: *"Sekilab CRDDC 2022 (Road Damage Detection Challenge 2022)"*.

### 2.2 Jaipur Municipal Bus Dataset
- **Target Volume**: 200–500 carefully curated, high-resolution frames captured from Jaipur City Transport Service Limited (JCTSL) scheduled routes.
- **Provenance**: Forward-facing 1080p 30fps camera mounted on bus dashboard behind wiper sweep.
- **Privacy Prerequisites**:
  - Municipal transport pilot consent verified.
  - Zero raw public imagery: Automated edge blurring applied to all human faces and vehicle registration plates prior to dataset compilation.
  - Storage location: `data/local/jaipur/` (strictly excluded from version control).
- **OSM Attribution**: When geographical road coordinate benchmarks are cross-referenced with OpenStreetMap vectors, attribution must state: *"© OpenStreetMap contributors"*.

### 2.3 COCO-Pretrained Backbone
- **Role**: General road scene object recognition (`vehicle`, `car`, `bus`, `truck`, `two_wheeler`, `pedestrian`, `signboard`).
- **Mapping**: Resolved via `ml.datasets.coco.map_coco_id_to_class()`.
- **Mandatory Attribution**: *"Lin et al., Microsoft COCO: Common Objects in Context, ECCV 2014"*.

### 2.4 Optional Restricted Datasets (IDD / Roboflow)
- **India Driving Dataset (IDD)**: Academic non-commercial license from IIIT Hyderabad. Requires institutional registration.
- **Roboflow Universe Candidates**: Must be individually vetted for terms.
- **Gating Mechanism**: Programmatically blocked by `DatasetManifest.require_dataset()` which raises `LicenseVerificationError` if `license_verified` is False.

---

## 3. Route/Day-Aware Split Protocol (Anti-Leakage)

> [!IMPORTANT]
> **No Random Frame Splitting**: Dashcam frames sampled from continuous video streams exhibit massive spatio-temporal redundancy. Random frame-level splits result in severe data leakage where nearly identical adjacent frames appear in both train and validation sets, producing artificially inflated evaluation metrics.

### Splitting Engine (`ml.datasets.split.RouteDaySplitter`)
1. **Grouping Unit**: Composite key `(route_id, capture_day)`.
2. **Distribution**:
   - **Train**: 70% of route/day groups.
   - **Validation**: 15% of distinct route/day groups (unseen routes or dates).
   - **Test / Benchmark**: 15% of distinct route/day groups.
3. **Guarantee**: Deterministic hashing assigns entire groups to a single split, guaranteeing zero frame intersection across partitions.

---

## 4. Annotation Validation Protocol

Before any dataset can transition from `DOWNLOADED` or `ANNOTATED` to `VALIDATED`, it must pass `ml.datasets.validator.validate_dataset_directory()`:

1. **Bounding Box Bounds**: Coordinates must be normalized in `[0.0, 1.0]`. Non-positive width or height is rejected.
2. **Class Consistency**: Class IDs must belong to the declared class taxonomy.
3. **Image-Label Parity**: Every `.txt` must have a corresponding `.jpg`/`.png`, and vice versa.
4. **Data Integrity**: Zero-byte or unreadable image files are flagged as fatal errors.

---

## 5. How to Ingest a Future Jaipur Dataset

Follow these steps when local road recordings become available:

1. **Initialize Directory Skeleton**:
   ```python
   from pathlib import Path
   from ml.datasets.jaipur import JaipurDatasetLayout

   layout = JaipurDatasetLayout(Path("data/local/jaipur"))
   layout.initialize_structure()
   ```
2. **Anonymize & Curate Frames**:
   Place un-anonymized footage in `data/local/jaipur/raw/` (offline). Run edge privacy filter to produce blurred frames in `data/local/jaipur/processed/`.
3. **Annotate & Validate**:
   Generate YOLO `.txt` labels in `data/local/jaipur/labels/`. Run validator:
   ```python
   from ml.datasets.validator import validate_dataset_directory

   summary = validate_dataset_directory(
       images_dir="data/local/jaipur/images",
       labels_dir="data/local/jaipur/labels",
       allowed_class_ids={0, 1, 2, 3, 4, 5, 6, 7, 8},
   )
   assert summary.is_valid, f"Validation failed: {summary.issues}"
   ```
4. **Generate Leakage-Free Splits**:
   ```python
   from ml.datasets.split import RouteDaySplitter

   splitter = RouteDaySplitter(seed=42)
   # frames: list of (frame_id, route_id, capture_day)
   res = splitter.split(frames)
   res.save_to_dir("data/local/jaipur/splits")
   ```
5. **Update Manifest**:
   Update status in `ml/datasets/manifests/dataset_manifest.yaml` from `PLANNED` to `VALIDATED`.
