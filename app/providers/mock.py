from __future__ import annotations

import json
from collections.abc import AsyncIterator

from app.providers.base import LLMProvider, LLMRequest, LLMResponse


class MockLLMProvider(LLMProvider):
    provider_name = "mock"
    model_name = "mock-deterministic-v1"

    async def generate(self, request: LLMRequest) -> LLMResponse:
        schema_name = request.schema_name or "support_ticket"

        if schema_name == "action_plan":
            payload = {
                "goal": "Improve reliability for an AI-backed service",
                "steps": [
                    "Validate structured outputs before returning responses",
                    "Add retries and fallback handling for transient provider failures",
                    "Run evaluation checks before shipping prompt changes",
                ],
                "risk": "medium",
                "owner": "platform-engineering",
            }
        else:
            payload = {
                "title": "Review AI service response handling",
                "summary": "The service should validate structured LLM output, handle provider failures, and record request-level diagnostics.",
                "priority": "medium",
                "next_action": "Add validation, fallback handling, and evaluation checks.",
            }

        return LLMResponse(
            content=json.dumps(payload),
            provider=self.provider_name,
            model=self.model_name,
        )

    async def stream(self, request: LLMRequest) -> AsyncIterator[str]:
        message = (
            "This streaming response demonstrates a FastAPI pattern for returning "
            "incremental LLM output while keeping the provider behind a service boundary."
        )
        for token in message.split(" "):
            yield token + " "
