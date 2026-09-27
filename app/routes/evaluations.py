from __future__ import annotations

from fastapi import APIRouter

from app.models import EvaluationRequest, EvaluationSummary
from app.services.evaluation import evaluate_output

router = APIRouter(prefix="/v1", tags=["evaluation"])


@router.post("/evaluations/run", response_model=EvaluationSummary)
async def run_evaluation(payload: EvaluationRequest) -> EvaluationSummary:
    return evaluate_output(
        output=payload.output,
        required_terms=payload.required_terms,
        forbidden_terms=payload.forbidden_terms,
    )
