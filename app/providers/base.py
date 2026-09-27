from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass, field


@dataclass(frozen=True)
class LLMRequest:
    prompt: str
    schema_name: str | None = None
    context: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class LLMResponse:
    content: str
    provider: str
    model: str


class LLMProvider(ABC):
    provider_name: str
    model_name: str

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError

    async def stream(self, request: LLMRequest) -> AsyncIterator[str]:
        response = await self.generate(request)
        for token in response.content.split(" "):
            yield token + " "
