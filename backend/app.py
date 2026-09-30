"""
FleetSight FastAPI application factory.

Creates and configures the ASGI application with:
- CORS middleware (origins from config)
- Structured logging
- Health endpoint
- Versioned API routers
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.v1.router import v1_router
from backend.config import settings
from backend.logging_config import get_logger, setup_logging
from backend.schemas import HealthResponse

_APP_VERSION = "0.1.0"

logger = get_logger("app")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application startup / shutdown lifecycle."""
    setup_logging()
    logger.info(
        "FleetSight starting - env=%s, debug=%s",
        settings.app_env,
        settings.app_debug,
    )
    # Seed initial demo corridor data if store is empty
    from backend.analytics.store import store
    if not store.issues:
        from scripts.seed_demo_data import seed_jaipur_demo_data
        seed_jaipur_demo_data()
        logger.info("Seeded initial Jaipur corridor demo data.")
    yield
    logger.info("FleetSight shutting down.")


def create_app() -> FastAPI:
    """Application factory — returns a fully configured FastAPI instance."""
    app = FastAPI(
        title="FleetSight",
        description="AI-powered mobile urban intelligence platform",
        version=_APP_VERSION,
        debug=settings.app_debug,
        lifespan=lifespan,
    )

    # --- CORS ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Health ---
    @app.get("/health", response_model=HealthResponse, tags=["system"])
    async def health() -> HealthResponse:
        return HealthResponse(version=_APP_VERSION, environment=settings.app_env)

    # --- API v1 ---
    app.include_router(v1_router)

    return app


app = create_app()
