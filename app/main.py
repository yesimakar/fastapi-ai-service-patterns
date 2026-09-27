from __future__ import annotations

from fastapi import FastAPI

from app.config import load_settings
from app.logging import configure_logging, log_event
from app.middleware import RequestIDMiddleware
from app.providers.factory import create_provider
from app.routes import evaluations, guardrails, health, stream, structured, tools
from app.services.ai_service import AIService
from app.services.tool_registry import ToolRegistry


def create_app() -> FastAPI:
    settings = load_settings()
    configure_logging(settings.log_level)

    provider = create_provider(settings.provider, settings)
    fallback_provider = create_provider(settings.fallback_provider, settings)

    app = FastAPI(
        title="FastAPI AI Service Patterns",
        version="0.1.0",
        description="Production-style FastAPI patterns for LLM-backed services.",
    )
    app.add_middleware(RequestIDMiddleware)

    app.state.provider = provider
    app.state.fallback_provider = fallback_provider
    app.state.ai_service = AIService(
        provider=provider,
        fallback_provider=fallback_provider,
        max_retries=settings.max_retries,
    )
    app.state.tool_registry = ToolRegistry()

    app.include_router(health.router)
    app.include_router(structured.router)
    app.include_router(stream.router)
    app.include_router(guardrails.router)
    app.include_router(evaluations.router)
    app.include_router(tools.router)

    log_event("app_started", provider=provider.provider_name, model=provider.model_name)
    return app


app = create_app()
