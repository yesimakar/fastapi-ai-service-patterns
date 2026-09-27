from __future__ import annotations

import json
from typing import Any

from pydantic import ValidationError

from app.models import ActionPlan, SchemaName, SupportTicket

SCHEMA_MODELS = {
    SchemaName.support_ticket: SupportTicket,
    SchemaName.action_plan: ActionPlan,
}


def validate_structured_output(schema_name: SchemaName, raw_output: str) -> tuple[dict[str, Any] | None, str | None]:
    try:
        payload = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc.msg}"

    model = SCHEMA_MODELS[schema_name]

    try:
        parsed = model.model_validate(payload)
    except ValidationError as exc:
        return None, exc.json()

    return parsed.model_dump(), None
