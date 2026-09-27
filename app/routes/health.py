from __future__ import annotations

from fastapi import APIRouter

from app.models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(service="fastapi-ai-service-patterns", status="ok", version="0.1.0")
