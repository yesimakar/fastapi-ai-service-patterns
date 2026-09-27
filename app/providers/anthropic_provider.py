from __future__ import annotations

from app.providers.base import LLMProvider, LLMRequest, LLMResponse


class AnthropicProvider(LLMProvider):
    provider_name = "anthropic"

    def __init__(self, api_key: str, model: str = "claude-3-5-haiku-latest") -> None:
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is required for the Anthropic provider")
        self.api_key = api_key
        self.model_name = model

    async def generate(self, request: LLMRequest) -> LLMResponse:
        try:
            from anthropic import AsyncAnthropic
        except ImportError as exc:
            raise RuntimeError("Install optional dependencies with: uv sync --dev --extra llm") from exc

        client = AsyncAnthropic(api_key=self.api_key)
        response = await client.messages.create(
            model=self.model_name,
            max_tokens=800,
            messages=[{"role": "user", "content": request.prompt}],
        )
        text_blocks = [block.text for block in response.content if getattr(block, "type", None) == "text"]
        return LLMResponse(content="\n".join(text_blocks), provider=self.provider_name, model=self.model_name)
