from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def with_retries(operation: Callable[[], Awaitable[T]], max_retries: int) -> T:
    attempt = 0
    last_error: Exception | None = None

    while attempt <= max_retries:
        try:
            return await operation()
        except Exception as exc:  # pragma: no cover - defensive retry wrapper
            last_error = exc
            attempt += 1
            if attempt > max_retries:
                break
            await asyncio.sleep(min(0.1 * attempt, 0.5))

    assert last_error is not None
    raise last_error
