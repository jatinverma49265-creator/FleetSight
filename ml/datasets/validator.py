"""
Annotation and Dataset Validation Utilities.

Validates YOLO format bounding box annotations, verifies paired image-label existence,
detects corrupted/empty files, and ensures all class IDs adhere to specified taxonomies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


@dataclass(frozen=True, slots=True)
class YOLOAnnotation:
    """A validated single-line YOLO bounding box annotation."""

    class_id: int
    x_center: float
    y_center: float
    width: float
    height: float


@dataclass(frozen=True)
class ValidationIssue:
    """A single diagnostic issue found during annotation validation."""

    level: str  # "ERROR" or "WARNING"
    file_path: str
    line_number: int | None
    message: str


@dataclass
class ValidationSummary:
    """Comprehensive summary of dataset validation results."""

    total_images: int = 0
    total_labels: int = 0
    total_boxes: int = 0
    empty_labels: int = 0
    missing_images: int = 0
    missing_labels: int = 0
    corrupt_images: int = 0
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Returns True if there are zero ERROR-level issues."""
        return not any(i.level == "ERROR" for i in self.issues)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.level == "ERROR")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.level == "WARNING")


def parse_yolo_line(
    line: str,
    line_number: int = 1,
    file_path: str = "",
    allowed_class_ids: set[int] | None = None,
) -> tuple[YOLOAnnotation | None, list[ValidationIssue]]:
    """
    Parse and validate a single space-separated line of a YOLO annotation file.

    Format expected: <class_id> <x_center> <y_center> <width> <height>
    Coordinates must be normalized in the range [0.0, 1.0].
    """
    issues: list[ValidationIssue] = []
    tokens = line.strip().split()
    if not tokens:
        return None, issues

    if len(tokens) != 5:
        msg = f"Malformed annotation: expected 5 tokens, found {len(tokens)}: '{line.strip()}'"
        issues.append(
            ValidationIssue(
                level="ERROR",
                file_path=file_path,
                line_number=line_number,
                message=msg,
            )
        )
        return None, issues


    try:
        class_id = int(tokens[0])
    except ValueError:
        issues.append(
            ValidationIssue(
                level="ERROR",
                file_path=file_path,
                line_number=line_number,
                message=f"Invalid class ID: '{tokens[0]}' is not an integer",
            )
        )
        return None, issues

    if class_id < 0:
        issues.append(
            ValidationIssue(
                level="ERROR",
                file_path=file_path,
                line_number=line_number,
                message=f"Class ID cannot be negative: {class_id}",
            )
        )

    if allowed_class_ids is not None and class_id not in allowed_class_ids:
        issues.append(
            ValidationIssue(
                level="ERROR",
                file_path=file_path,
                line_number=line_number,
                message=f"Class ID {class_id} not in allowed class IDs {sorted(allowed_class_ids)}",
            )
        )

    try:
        x_c, y_c, w, h = (float(tokens[1]), float(tokens[2]), float(tokens[3]), float(tokens[4]))
    except ValueError:
        issues.append(
            ValidationIssue(
                level="ERROR",
                file_path=file_path,
                line_number=line_number,
                message=f"Malformed bounding box coordinates in: '{line.strip()}'",
            )
        )
        return None, issues

    # Validate coordinate normalization [0.0, 1.0]
    for val, name in [(x_c, "x_center"), (y_c, "y_center"), (w, "width"), (h, "height")]:
        if not (0.0 <= val <= 1.0):
            issues.append(
                ValidationIssue(
                    level="ERROR",
                    file_path=file_path,
                    line_number=line_number,
                    message=f"Coordinate {name}={val} out of normalized bounds [0.0, 1.0]",
                )
            )

    if w <= 0.0 or h <= 0.0:
        issues.append(
            ValidationIssue(
                level="ERROR",
                file_path=file_path,
                line_number=line_number,
                message=f"Non-positive box dimension: width={w}, height={h}",
            )
        )

    if issues:
        return None, issues

    return YOLOAnnotation(class_id=class_id, x_center=x_c, y_center=y_c, width=w, height=h), issues


def validate_annotation_file(
    file_path: Path | str,
    allowed_class_ids: set[int] | None = None,
    allow_empty: bool = True,
) -> tuple[list[YOLOAnnotation], list[ValidationIssue]]:
    """
    Validate an entire YOLO .txt annotation file.

    Returns:
        (valid_annotations, issues_list)
    """
    path = Path(file_path)
    issues: list[ValidationIssue] = []
    annotations: list[YOLOAnnotation] = []

    if not path.exists():
        issues.append(
            ValidationIssue(
                level="ERROR",
                file_path=str(path),
                line_number=None,
                message="Annotation file does not exist",
            )
        )
        return annotations, issues

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        issues.append(
            ValidationIssue(
                level="ERROR",
                file_path=str(path),
                line_number=None,
                message=f"Could not read annotation file: {e}",
            )
        )
        return annotations, issues

    lines = [line for line in content.splitlines() if line.strip()]
    if not lines:
        if not allow_empty:
            issues.append(
                ValidationIssue(
                    level="ERROR",
                    file_path=str(path),
                    line_number=None,
                    message="Annotation file is empty",
                )
            )
        else:
            issues.append(
                ValidationIssue(
                    level="WARNING",
                    file_path=str(path),
                    line_number=None,
                    message="Annotation file has zero objects (background frame)",
                )
            )
        return annotations, issues

    for idx, line in enumerate(lines, start=1):
        ann, line_issues = parse_yolo_line(
            line,
            line_number=idx,
            file_path=str(path),
            allowed_class_ids=allowed_class_ids,
        )
        issues.extend(line_issues)
        if ann is not None:
            annotations.append(ann)

    return annotations, issues


def validate_dataset_directory(
    images_dir: Path | str,
    labels_dir: Path | str,
    allowed_class_ids: set[int] | None = None,
    allow_empty_labels: bool = True,
) -> ValidationSummary:
    """
    Validate a paired directory of images and YOLO label files.
    """
    img_dir = Path(images_dir)
    lbl_dir = Path(labels_dir)
    summary = ValidationSummary()

    if not img_dir.exists():
        summary.issues.append(
            ValidationIssue(
                level="ERROR",
                file_path=str(img_dir),
                line_number=None,
                message="Images directory missing",
            )
        )
        return summary

    if not lbl_dir.exists():
        summary.issues.append(
            ValidationIssue(
                level="ERROR",
                file_path=str(lbl_dir),
                line_number=None,
                message="Labels directory missing",
            )
        )
        return summary

    image_files = {
        p.stem: p
        for p in img_dir.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    }
    label_files = {
        p.stem: p for p in lbl_dir.iterdir() if p.is_file() and p.suffix.lower() == ".txt"
    }

    summary.total_images = len(image_files)
    summary.total_labels = len(label_files)

    # Check for corrupt or zero-byte images
    for img_path in image_files.values():
        if img_path.stat().st_size == 0:
            summary.corrupt_images += 1
            summary.issues.append(
                ValidationIssue(
                    level="ERROR",
                    file_path=str(img_path),
                    line_number=None,
                    message="Image file is 0 bytes (corrupt/empty)",
                )
            )

    # Check for missing label files (images without labels)
    for stem, img_path in image_files.items():
        if stem not in label_files:
            summary.missing_labels += 1
            summary.issues.append(
                ValidationIssue(
                    level="WARNING",
                    file_path=str(img_path),
                    line_number=None,
                    message=f"Missing corresponding label file: {lbl_dir / (stem + '.txt')}",
                )
            )

    # Check for missing images (labels without images)
    for stem, lbl_path in label_files.items():
        if stem not in image_files:
            summary.missing_images += 1
            summary.issues.append(
                ValidationIssue(
                    level="ERROR",
                    file_path=str(lbl_path),
                    line_number=None,
                    message="Label file has no corresponding image in images directory",
                )
            )

    # Validate each label file
    for lbl_path in label_files.values():
        anns, issues = validate_annotation_file(
            lbl_path,
            allowed_class_ids=allowed_class_ids,
            allow_empty=allow_empty_labels,
        )

        summary.issues.extend(issues)
        summary.total_boxes += len(anns)
        if not anns and any(
            i.message.startswith("Annotation file has zero objects") for i in issues
        ):
            summary.empty_labels += 1

    return summary
