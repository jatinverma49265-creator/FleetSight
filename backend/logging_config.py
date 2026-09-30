"""
Structured logging setup for FleetSight.

Produces JSON-formatted log lines in production and human-readable
output in development.  Configured via APP_LOG_LEVEL env var.
"""

from __future__ import annotations

import logging
import sys

from backend.config import settings


def setup_logging() -> None:
    """Configure the root logger once at application startup."""
    level = getattr(logging, settings.app_log_level.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    if settings.app_env == "production":
        # Machine-readable JSON lines in production.
        fmt = (
            '{"time":"%(asctime)s","level":"%(levelname)s",'
            '"logger":"%(name)s","message":"%(message)s"}'
        )
    else:
        fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    handler.setFormatter(logging.Formatter(fmt))

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a child logger with the given name."""
    return logging.getLogger(f"fleetsight.{name}")
