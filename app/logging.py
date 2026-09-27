from __future__ import annotations

import json
import logging
from typing import Any

from app.utils.redaction import redact_mapping


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level.upper(),
        format="%(message)s",
    )


def log_event(event: str, **fields: Any) -> None:
    safe_fields = redact_mapping(fields)
    logging.getLogger("fastapi-ai-service-patterns").info(
        json.dumps({"event": event, **safe_fields}, sort_keys=True)
    )
