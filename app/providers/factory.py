from __future__ import annotations

from app.config import Settings
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.base import LLMProvider
from app.providers.mock import MockLLMProvider
from app.providers.openai_provider import OpenAIProvider


def create_provider(name: str, settings: Settings) -> LLMProvider:
    normalized = name.lower().strip()

    if normalized == "mock":
        return MockLLMProvider()

    if normalized == "openai":
        return OpenAIProvider(api_key=settings.openai_api_key, model=settings.model)

    if normalized == "anthropic":
        return AnthropicProvider(api_key=settings.anthropic_api_key, model=settings.model)

    raise ValueError(f"unsupported provider: {name}")
