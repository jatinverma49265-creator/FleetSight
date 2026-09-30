"""
Machine-readable dataset manifest for FleetSight.

Tracks dataset provenance, license, class taxonomy, download instructions,
and current status without committing large dataset files.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

from ml.datasets.exceptions import (
    DatasetNotFoundError,
    DatasetNotReadyError,
    LicenseVerificationError,
)

DEFAULT_MANIFEST_PATH = Path(__file__).resolve().parent / "manifests" / "dataset_manifest.yaml"


class DatasetType(StrEnum):
    """
    Categorization of data origins to prevent data contamination.

    Rules:
    - PUBLIC_BENCHMARK: Open public benchmark datasets (e.g. RDD2022, COCO).
    - REAL_LOCAL: Primary on-bus video collected in target geography (Jaipur).
    - SIMULATED: Synthetically created test vectors for offline testing.
    - OPTIONAL_RESTRICTED: Secondary candidate datasets with license gating (e.g. IDD, Roboflow).
    """

    PUBLIC_BENCHMARK = "public_benchmark"
    REAL_LOCAL = "real_local"
    SIMULATED = "simulated"
    OPTIONAL_RESTRICTED = "optional_restricted"


class DatasetStatus(StrEnum):
    """
    Status of a dataset in the FleetSight pipeline.

    Rules:
    - PLANNED: Dataset identified and planned, not yet acquired.
    - AVAILABLE: Public weights or repository checkpoints accessible.
    - DOWNLOADED: Downloaded locally on disk (verified).
    - ANNOTATED: Locally labeled and formatted for training.
    - VALIDATED: Passed quality/annotation validator checks.
    - REJECTED: Failed license or quality checks; prohibited from use.
    """

    PLANNED = "PLANNED"
    AVAILABLE = "AVAILABLE"
    DOWNLOADED = "DOWNLOADED"
    ANNOTATED = "ANNOTATED"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"


class DatasetManifestEntry(BaseModel):
    """Metadata specification for a single dataset source."""

    dataset_name: str = Field(..., min_length=1)
    version: str = Field(..., min_length=1)
    dataset_type: DatasetType = Field(default=DatasetType.PUBLIC_BENCHMARK)
    source: str = Field(..., description="Upstream URL, DOI, or collection organization")
    license: str = Field(..., description="e.g. CC BY-SA 4.0, Commercial Restricted")
    purpose: str = Field(..., description="Role in FleetSight (e.g. road damage baseline)")
    classes: list[str] = Field(default_factory=list)
    local_path: str = Field(default="", description="Relative path under data/")
    download_instructions: str = Field(..., description="Step-by-step instructions or command")
    provenance: str = Field(..., description="Collection methodology and origin")
    status: DatasetStatus = Field(default=DatasetStatus.PLANNED)

    # Privacy & Governance
    license_verified: bool = Field(
        default=False,
        description="Whether restricted/academic licenses have been verified",
    )
    face_blurring_required: bool = Field(
        default=False,
        description="Must apply privacy de-identification before model training/serving",
    )
    consent_required: bool = Field(
        default=False,
        description="Requires municipal or transport authority data sharing consent",
    )
    attribution_required: str = Field(
        default="",
        description="Mandatory citation string for documentation/publications",
    )

    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="ignore")


class DatasetManifest(BaseModel):
    """Collection of dataset manifest entries."""

    schema_version: str = "1.0.0"
    datasets: list[DatasetManifestEntry] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore")

    def get_dataset(self, name: str) -> DatasetManifestEntry | None:
        """Find entry by name (case-insensitive)."""
        target = name.lower()
        for entry in self.datasets:
            if entry.dataset_name.lower() == target:
                return entry
        return None

    def require_dataset(
        self,
        name: str,
        base_dir: Path | str = "",
        min_status: DatasetStatus | None = None,
    ) -> DatasetManifestEntry:
        """
        Retrieve a registered dataset, enforcing registration and readiness checks.

        Raises:
            DatasetNotFoundError: If dataset is unknown or missing from disk.
            LicenseVerificationError: If dataset requires license check and is unverified.
            DatasetNotReadyError: If dataset has not achieved min_status.
        """
        entry = self.get_dataset(name)
        if entry is None:
            raise DatasetNotFoundError(
                dataset_name=name,
                instructions="Register dataset in ml/datasets/manifests/dataset_manifest.yaml",
            )

        if entry.dataset_type == DatasetType.OPTIONAL_RESTRICTED and not entry.license_verified:
            raise LicenseVerificationError(
                dataset_name=entry.dataset_name,
                license_info=entry.license,
                reason="Institutional access authorization must be confirmed before use.",
            )

        if min_status is not None:
            status_order = [
                DatasetStatus.PLANNED,
                DatasetStatus.AVAILABLE,
                DatasetStatus.DOWNLOADED,
                DatasetStatus.ANNOTATED,
                DatasetStatus.VALIDATED,
            ]
            current_idx = status_order.index(entry.status) if entry.status in status_order else -1
            required_idx = status_order.index(min_status) if min_status in status_order else -1
            if current_idx < required_idx:
                raise DatasetNotReadyError(
                    dataset_name=entry.dataset_name,
                    current_status=entry.status.value,
                    required_status=min_status.value,
                )

        if base_dir and entry.local_path:
            resolved = (Path(base_dir) / entry.local_path).resolve()
            if not resolved.exists():
                raise DatasetNotFoundError(
                    dataset_name=entry.dataset_name,
                    local_path=str(resolved),
                    instructions=entry.download_instructions,
                )

        return entry

    @classmethod
    def load_from_yaml(cls, path: Path | str) -> DatasetManifest:
        """Load manifest from a YAML file."""
        filepath = Path(path)
        if not filepath.exists():
            raise FileNotFoundError(f"Manifest file not found: {filepath}")
        with filepath.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)

    def save_to_yaml(self, path: Path | str) -> None:
        """Save manifest to a YAML file."""
        filepath = Path(path)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open("w", encoding="utf-8") as f:
            yaml.safe_dump(self.model_dump(mode="json"), f, sort_keys=False)

    def verify_local_status(self, base_dir: Path | str) -> dict[str, DatasetStatus]:
        """
        Verify real filesystem existence of datasets marked DOWNLOADED or ANNOTATED.

        Never claim a dataset is available locally unless its local_path exists.
        Returns a mapping of dataset_name -> actual verified status.
        """
        base = Path(base_dir)
        verified: dict[str, DatasetStatus] = {}

        for entry in self.datasets:
            if entry.status in (
                DatasetStatus.DOWNLOADED,
                DatasetStatus.ANNOTATED,
                DatasetStatus.VALIDATED,
            ):
                if not entry.local_path:
                    verified[entry.dataset_name] = DatasetStatus.PLANNED
                    continue
                resolved_path = (base / entry.local_path).resolve()
                if resolved_path.exists() and any(resolved_path.iterdir()):
                    verified[entry.dataset_name] = entry.status
                else:
                    verified[entry.dataset_name] = DatasetStatus.PLANNED
            else:
                verified[entry.dataset_name] = entry.status

        return verified


def load_default_manifest() -> DatasetManifest:
    """Load the project default dataset manifest."""
    return DatasetManifest.load_from_yaml(DEFAULT_MANIFEST_PATH)
