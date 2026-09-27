from __future__ import annotations

SENSITIVE_KEY_PARTS = (
    "token",
    "secret",
    "password",
    "api_key",
    "apikey",
    "authorization",
    "credential",
)


def redact_mapping(value: dict[str, object]) -> dict[str, object]:
    redacted: dict[str, object] = {}

    for key, item in value.items():
        normalized = key.lower()
        if any(part in normalized for part in SENSITIVE_KEY_PARTS):
            redacted[key] = "[redacted]"
        elif isinstance(item, dict):
            redacted[key] = redact_mapping(item)
        else:
            redacted[key] = item

    return redacted
