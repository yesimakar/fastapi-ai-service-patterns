from __future__ import annotations

from app.providers.base import LLMProvider, LLMRequest, LLMResponse


class OpenAIProvider(LLMProvider):
    provider_name = "openai"

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for the OpenAI provider")
        self.api_key = api_key
        self.model_name = model

    async def generate(self, request: LLMRequest) -> LLMResponse:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise RuntimeError("Install optional dependencies with: uv sync --dev --extra llm") from exc

        client = AsyncOpenAI(api_key=self.api_key)
        response = await client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "Return concise, production-oriented responses."},
                {"role": "user", "content": request.prompt},
            ],
        )
        content = response.choices[0].message.content or ""
        return LLMResponse(content=content, provider=self.provider_name, model=self.model_name)
