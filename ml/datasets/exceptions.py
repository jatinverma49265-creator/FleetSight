"""
FleetSight Dataset & ML Pipeline Exceptions.

Structured exception hierarchy for dataset management, license safety,
annotation validation, and missing asset handling.
"""

from __future__ import annotations


class DatasetError(Exception):
    """Base exception for all dataset pipeline errors."""


class DatasetNotFoundError(DatasetError):
    """
    Raised when a requested dataset is not registered or not found on disk.

    Provides actionable resolution instructions without attempting uncontrolled downloads.
    """

    def __init__(self, dataset_name: str, local_path: str = "", instructions: str = "") -> None:
        self.dataset_name = dataset_name
        self.local_path = local_path
        self.instructions = instructions
        msg = f"Dataset '{dataset_name}' is not available locally."
        if local_path:
            msg += f" Expected location: {local_path}."
        if instructions:
            msg += f" Instructions: {instructions}"
        super().__init__(msg)


class DatasetNotReadyError(DatasetError):
    """
    Raised when a dataset exists on disk but is not in the required status
    (e.g., PLANNED or DOWNLOADED when VALIDATED is required for training).
    """

    def __init__(self, dataset_name: str, current_status: str, required_status: str) -> None:
        self.dataset_name = dataset_name
        self.current_status = current_status
        self.required_status = required_status
        super().__init__(
            f"Dataset '{dataset_name}' status is {current_status}; "
            f"must be {required_status} before proceeding."
        )


class LicenseVerificationError(DatasetError):
    """
    Raised when an optional or restricted dataset is accessed without verified
    institutional authorization or license compliance.
    """

    def __init__(self, dataset_name: str, license_info: str, reason: str = "") -> None:
        self.dataset_name = dataset_name
        self.license_info = license_info
        msg = (
            f"Dataset '{dataset_name}' requires institutional license verification "
            f"under '{license_info}' before it can be processed or trained on."
        )
        if reason:
            msg += f" Reason: {reason}"
        super().__init__(msg)


class AnnotationValidationError(DatasetError):
    """Raised when annotations fail schema, bounding box, or image consistency checks."""


class ModelWeightsMissingError(FileNotFoundError):
    """
    Raised when detector weights do not exist on disk.

    Prevents automatic or uncontrolled downloads of large binary checkpoints.
    """

    def __init__(self, model_name: str, weights_path: str) -> None:
        self.model_name = model_name
        self.weights_path = weights_path
        super().__init__(
            f"Weights not found: {weights_path}. "
            f"Model weights for '{model_name}' not found at '{weights_path}'. "
            f"FleetSight does not automatically download weights. "
            f"Please verify weights location or run the designated setup script."
        )
