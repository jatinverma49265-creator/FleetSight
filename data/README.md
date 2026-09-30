# FleetSight Data Directory Structure

This directory houses the offline dataset directory structure. In accordance with strict repository engineering hygiene, no raw datasets, large archives, images, or video files are committed to version control.

## Subdirectories:
- `raw/`: Unprocessed incoming footage, raw dashcam recordings, and upstream dataset archives.
- `processed/`: Processed, resized, and privacy-anonymized (face/plate blurred) image frames.
- `annotations/`: Validated bounding box label files in standard YOLO/COCO format.
- `manifests/`: Dataset manifests and provenance declarations.
- `splits/`: Route- and day-aware split index files (`train.txt`, `val.txt`, `test.txt`).
- `local/`: Local, privately collected Jaipur transport bus recordings (restricted access).
