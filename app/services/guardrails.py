from __future__ import annotations

from app.models import GuardrailResult, RiskLevel

INJECTION_PATTERNS = (
    "ignore previous instructions",
    "ignore all previous instructions",
    "reveal the system prompt",
    "show me the system prompt",
    "developer message",
    "exfiltrate",
    "jailbreak",
    "bypass safety",
)

HIGH_RISK_PATTERNS = (
    "delete all",
    "drop database",
    "disable authentication",
    "send secrets",
)


def check_text(text: str) -> GuardrailResult:
    normalized = text.lower()
    reasons: list[str] = []

    for pattern in INJECTION_PATTERNS:
        if pattern in normalized:
            reasons.append(f"prompt-injection pattern detected: {pattern}")

    for pattern in HIGH_RISK_PATTERNS:
        if pattern in normalized:
            reasons.append(f"high-risk operational instruction detected: {pattern}")

    if any("high-risk" in reason for reason in reasons):
        return GuardrailResult(allowed=False, risk_level=RiskLevel.high, reasons=reasons)

    if reasons:
        return GuardrailResult(allowed=False, risk_level=RiskLevel.medium, reasons=reasons)

    return GuardrailResult(allowed=True, risk_level=RiskLevel.low, reasons=[])
