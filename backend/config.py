"""
FleetSight application configuration.

All settings are loaded from environment variables (or a .env file in development).
No secrets are hard-coded.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Root application settings, populated from environment / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    app_env: str = Field(default="development", description="development | staging | production")
    app_debug: bool = Field(default=False)
    app_log_level: str = Field(default="INFO")

    # --- Backend ---
    backend_host: str = Field(default="0.0.0.0")
    backend_port: int = Field(default=8000)
    backend_cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
    )

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                import json

                try:
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return [str(item) for item in parsed]
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        if isinstance(v, (list, tuple)):
            return [str(item) for item in v]
        return ["http://localhost:3000", "http://localhost:5173"]

    # --- Database ---
    database_url: str = Field(
        default="postgresql+asyncpg://fleetsight:changeme@localhost:5432/fleetsight",
        description="Async SQLAlchemy database URL",
    )

    # --- ML ---
    fleetsight_detector_family: str = Field(
        default="ultralytics",
        description="Detector model family (e.g. ultralytics)",
    )
    fleetsight_detector_model: str = Field(
        default="yolo11",
        description="Detector backend identifier (yolo11 | yolo12 | yolo26)",
    )
    fleetsight_detector_weights_path: str = Field(default="")
    fleetsight_detector_confidence_threshold: float = Field(default=0.25)
    fleetsight_detector_device: str = Field(default="cpu")

    # --- Privacy ---
    privacy_blur_faces: bool = Field(default=True)
    privacy_blur_plates: bool = Field(default=True)


# Singleton – import this instance everywhere.
settings = Settings()
