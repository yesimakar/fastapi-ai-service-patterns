from __future__ import annotations

from fastapi import APIRouter, Request

from app.models import StructuredGenerateRequest, StructuredGenerateResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/v1", tags=["structured-output"])


@router.post("/structured-output", response_model=StructuredGenerateResponse)
async def structured_output(request: Request, payload: StructuredGenerateRequest) -> StructuredGenerateResponse:
    service: AIService = request.app.state.ai_service
    return await service.generate_structured(request.state.request_id, payload)
