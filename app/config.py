from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    provider: str = "mock"
    fallback_provider: str = "mock"
    model: str = "mock-deterministic-v1"
    log_level: str = "INFO"
    max_retries: int = 2
    request_timeout_seconds: float = 10.0
    openai_api_key: str = ""
    anthropic_api_key: str = ""


def load_settings() -> Settings:
    return Settings(
        provider=os.getenv("AI_SERVICE_PROVIDER", "mock"),
        fallback_provider=os.getenv("AI_SERVICE_FALLBACK_PROVIDER", "mock"),
        model=os.getenv("AI_SERVICE_MODEL", "mock-deterministic-v1"),
        log_level=os.getenv("AI_SERVICE_LOG_LEVEL", "INFO"),
        max_retries=_get_int("AI_SERVICE_MAX_RETRIES", 2),
        request_timeout_seconds=_get_float("AI_SERVICE_REQUEST_TIMEOUT_SECONDS", 10.0),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
    )


def _get_int(key: str, default: int) -> int:
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _get_float(key: str, default: float) -> float:
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default
