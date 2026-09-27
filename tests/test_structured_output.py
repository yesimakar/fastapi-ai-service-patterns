import json

from app.models import SchemaName
from app.services.structured_output import validate_structured_output


def test_valid_support_ticket_output():
    raw = json.dumps(
        {
            "title": "Review AI output validation",
            "summary": "The service should validate structured output before returning it.",
            "priority": "medium",
            "next_action": "Add schema validation.",
        }
    )

    parsed, error = validate_structured_output(SchemaName.support_ticket, raw)

    assert error is None
    assert parsed is not None
    assert parsed["priority"] == "medium"


def test_invalid_json_returns_error():
    parsed, error = validate_structured_output(SchemaName.support_ticket, "not-json")

    assert parsed is None
    assert error is not None
