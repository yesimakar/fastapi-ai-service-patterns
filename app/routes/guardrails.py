from __future__ import annotations

from fastapi import APIRouter

from app.models import GuardrailCheckRequest, GuardrailResult
from app.services.guardrails import check_text

router = APIRouter(prefix="/v1", tags=["guardrails"])


@router.post("/guardrails/check", response_model=GuardrailResult)
async def guardrail_check(payload: GuardrailCheckRequest) -> GuardrailResult:
    return check_text(payload.text)
