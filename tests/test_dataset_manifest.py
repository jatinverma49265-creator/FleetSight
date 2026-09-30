"""Tests for Dataset Manifest, metadata provenance, and missing-dataset safety."""

from __future__ import annotations

from pathlib import Path

import pytest

from ml.datasets.exceptions import (
    DatasetNotFoundError,
    DatasetNotReadyError,
    LicenseVerificationError,
)
from ml.datasets.manifest import (
    DatasetManifest,
    DatasetManifestEntry,
    DatasetStatus,
    DatasetType,
    load_default_manifest,
)


class TestDatasetManifest:
    def test_load_default_manifest(self) -> None:
        manifest = load_default_manifest()
        assert manifest.schema_version == "1.0.0"
        assert len(manifest.datasets) >= 5

        # Check required core datasets are present
        names = [d.dataset_name for d in manifest.datasets]
        assert "rdd2022" in names
        assert "jaipur_custom" in names
        assert "coco_pretrained" in names
        assert "idd_india_driving_dataset" in names
        assert "simulated_demo" in names

    def test_dataset_provenance_and_licensing_fields(self) -> None:
        manifest = load_default_manifest()
        for entry in manifest.datasets:
            assert entry.dataset_name
            assert entry.version
            assert entry.source
            assert entry.license
            assert entry.purpose
            assert entry.provenance
            assert entry.download_instructions
            assert isinstance(entry.status, DatasetStatus)
            assert isinstance(entry.dataset_type, DatasetType)

    def test_distinction_between_real_public_and_simulated(self) -> None:
        manifest = load_default_manifest()

        rdd = manifest.get_dataset("rdd2022")
        assert rdd is not None
        assert rdd.dataset_type == DatasetType.PUBLIC_BENCHMARK

        jaipur = manifest.get_dataset("jaipur_custom")
        assert jaipur is not None
        assert jaipur.dataset_type == DatasetType.REAL_LOCAL
        assert jaipur.face_blurring_required is True
        assert jaipur.consent_required is True

        sim = manifest.get_dataset("simulated_demo")
        assert sim is not None
        assert sim.dataset_type == DatasetType.SIMULATED
        assert sim.metadata.get("never_mix_with_benchmarks") is True

    def test_verify_local_status_downgrades_missing_data(self, tmp_path: Path) -> None:
        entry = DatasetManifestEntry(
            dataset_name="test_dataset",
            version="1.0",
            source="https://example.com",
            license="MIT",
            purpose="test",
            download_instructions="none",
            provenance="test",
            local_path="data/test_data",
            status=DatasetStatus.DOWNLOADED,
        )
        manifest = DatasetManifest(datasets=[entry])

        # Verification against empty directory must downgrade status to PLANNED
        verified = manifest.verify_local_status(base_dir=tmp_path)
        assert verified["test_dataset"] == DatasetStatus.PLANNED

        # If data folder actually exists and has files, preserve status
        target_dir = tmp_path / "data" / "test_data"
        target_dir.mkdir(parents=True)
        (target_dir / "sample.txt").write_text("dummy")

        verified_after = manifest.verify_local_status(base_dir=tmp_path)
        assert verified_after["test_dataset"] == DatasetStatus.DOWNLOADED

    def test_require_dataset_unknown_raises_not_found(self) -> None:
        manifest = load_default_manifest()
        with pytest.raises(
            DatasetNotFoundError, match="Dataset 'nonexistent_dataset' is not available"
        ):
            manifest.require_dataset("nonexistent_dataset")

    def test_require_dataset_unverified_license_raises_error(self) -> None:
        manifest = load_default_manifest()
        # idd requires license verification and license_verified is False
        with pytest.raises(
            LicenseVerificationError, match="requires institutional license verification"
        ):
            manifest.require_dataset("idd_india_driving_dataset")

    def test_require_dataset_status_not_met_raises_error(self) -> None:
        manifest = load_default_manifest()
        # rdd2022 status is PLANNED; requiring VALIDATED should fail
        with pytest.raises(DatasetNotReadyError, match="must be VALIDATED before proceeding"):
            manifest.require_dataset("rdd2022", min_status=DatasetStatus.VALIDATED)

    def test_manifest_yaml_roundtrip(self, tmp_path: Path) -> None:
        manifest = load_default_manifest()
        yaml_out = tmp_path / "test_manifest.yaml"
        manifest.save_to_yaml(yaml_out)
        assert yaml_out.exists()

        reloaded = DatasetManifest.load_from_yaml(yaml_out)
        assert len(reloaded.datasets) == len(manifest.datasets)
        assert reloaded.schema_version == manifest.schema_version
