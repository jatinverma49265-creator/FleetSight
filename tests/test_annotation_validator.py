"""Tests for YOLO annotation validator and dataset integrity checks."""

from __future__ import annotations

from pathlib import Path

from ml.datasets.validator import (
    parse_yolo_line,
    validate_annotation_file,
    validate_dataset_directory,
)


class TestAnnotationValidator:
    def test_parse_valid_yolo_line(self) -> None:
        line = "0 0.5000 0.5000 0.2000 0.3000"
        ann, issues = parse_yolo_line(line, allowed_class_ids={0, 1})
        assert len(issues) == 0
        assert ann is not None
        assert ann.class_id == 0
        assert ann.x_center == 0.5
        assert ann.y_center == 0.5
        assert ann.width == 0.2
        assert ann.height == 0.3

    def test_parse_malformed_tokens(self) -> None:
        line = "0 0.5 0.5"  # only 3 tokens instead of 5
        ann, issues = parse_yolo_line(line)
        assert ann is None
        assert any("expected 5 tokens" in i.message for i in issues)

    def test_parse_invalid_class_id(self) -> None:
        # non-integer class
        ann1, issues1 = parse_yolo_line("pothole 0.5 0.5 0.2 0.2")
        assert ann1 is None
        assert any("not an integer" in i.message for i in issues1)

        # negative class
        ann2, issues2 = parse_yolo_line("-1 0.5 0.5 0.2 0.2")
        assert ann2 is None
        assert any("cannot be negative" in i.message for i in issues2)

        # disallowed class ID
        ann3, issues3 = parse_yolo_line("4 0.5 0.5 0.2 0.2", allowed_class_ids={0, 1, 2, 3})
        assert ann3 is None
        assert any("not in allowed class IDs" in i.message for i in issues3)

    def test_parse_out_of_bounds_coordinates(self) -> None:
        # x_center > 1.0
        ann, issues = parse_yolo_line("0 1.25 0.5 0.2 0.2")
        assert ann is None
        assert any("out of normalized bounds" in i.message for i in issues)

        # non-positive width
        ann2, issues2 = parse_yolo_line("0 0.5 0.5 0.0 0.2")
        assert ann2 is None
        assert any("Non-positive box dimension" in i.message for i in issues2)

    def test_validate_annotation_file(self, tmp_path: Path) -> None:
        txt_file = tmp_path / "sample.txt"
        txt_file.write_text(
            "0 0.4 0.4 0.1 0.1\n1 0.6 0.6 0.2 0.2\n",
            encoding="utf-8",
        )
        anns, issues = validate_annotation_file(txt_file, allowed_class_ids={0, 1})
        assert len(anns) == 2
        assert len([i for i in issues if i.level == "ERROR"]) == 0

        # Empty annotation file with allow_empty=False
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("", encoding="utf-8")
        anns_empty, issues_empty = validate_annotation_file(empty_file, allow_empty=False)
        assert len(anns_empty) == 0
        assert any("Annotation file is empty" in i.message for i in issues_empty)

    def test_validate_dataset_directory(self, tmp_path: Path) -> None:
        img_dir = tmp_path / "images"
        lbl_dir = tmp_path / "labels"
        img_dir.mkdir()
        lbl_dir.mkdir()

        # Valid pair 1
        (img_dir / "frame1.jpg").write_bytes(b"dummy_image_data")
        (lbl_dir / "frame1.txt").write_text("0 0.5 0.5 0.2 0.2\n")

        # Corrupt / 0-byte image
        (img_dir / "frame2.jpg").write_bytes(b"")
        (lbl_dir / "frame2.txt").write_text("0 0.5 0.5 0.2 0.2\n")

        # Missing label
        (img_dir / "frame3.jpg").write_bytes(b"dummy_image_data")

        # Missing image
        (lbl_dir / "frame4.txt").write_text("0 0.5 0.5 0.2 0.2\n")

        summary = validate_dataset_directory(img_dir, lbl_dir, allowed_class_ids={0})
        assert summary.total_images == 3
        assert summary.total_labels == 3
        assert summary.corrupt_images == 1
        assert summary.missing_labels == 1
        assert summary.missing_images == 1
        assert not summary.is_valid
