from __future__ import annotations

from app.models import (
    EvaluationSummary,
    GuardrailResult,
    SchemaName,
    StructuredGenerateRequest,
    StructuredGenerateResponse,
)
from app.providers.base import LLMProvider, LLMRequest
from app.services.evaluation import evaluate_structured_service_output
from app.services.guardrails import check_text
from app.services.retry import with_retries
from app.services.structured_output import validate_structured_output


class AIService:
    def __init__(
        self,
        provider: LLMProvider,
        fallback_provider: LLMProvider,
        max_retries: int,
    ) -> None:
        self.provider = provider
        self.fallback_provider = fallback_provider
        self.max_retries = max_retries

    async def generate_structured(
        self,
        request_id: str,
        request: StructuredGenerateRequest,
    ) -> StructuredGenerateResponse:
        guardrail = check_text("\n".join([request.prompt, *request.context]))
        if not guardrail.allowed:
            return StructuredGenerateResponse(
                request_id=request_id,
                provider=self.provider.provider_name,
                model=self.provider.model_name,
                schema_name=request.schema_name,
                raw_output="",
                parsed_output=None,
                validation_error="request blocked by guardrail",
                guardrail=guardrail,
                evaluation=EvaluationSummary(
                    passed=False,
                    score=0.0,
                    checks=["guardrail"],
                    failures=guardrail.reasons,
                ),
            )

        llm_request = LLMRequest(
            prompt=request.prompt,
            schema_name=request.schema_name.value,
            context=request.context,
        )

        try:
            response = await with_retries(lambda: self.provider.generate(llm_request), self.max_retries)
        except Exception:
            response = await self.fallback_provider.generate(llm_request)

        parsed_output, validation_error = validate_structured_output(request.schema_name, response.content)
        evaluation = None
        if request.enable_evaluation:
            evaluation = evaluate_structured_service_output(response.content, validation_error)

        return StructuredGenerateResponse(
            request_id=request_id,
            provider=response.provider,
            model=response.model,
            schema_name=request.schema_name,
            raw_output=response.content,
            parsed_output=parsed_output,
            validation_error=validation_error,
            guardrail=guardrail,
            evaluation=evaluation,
        )
