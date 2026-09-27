from __future__ import annotations

from app.models import EvaluationSummary


def evaluate_output(
    output: str,
    required_terms: list[str] | None = None,
    forbidden_terms: list[str] | None = None,
) -> EvaluationSummary:
    required_terms = required_terms or []
    forbidden_terms = forbidden_terms or []
    normalized = output.lower()

    checks: list[str] = []
    failures: list[str] = []

    for term in required_terms:
        checks.append(f"required term: {term}")
        if term.lower() not in normalized:
            failures.append(f"missing required term: {term}")

    for term in forbidden_terms:
        checks.append(f"forbidden term: {term}")
        if term.lower() in normalized:
            failures.append(f"contains forbidden term: {term}")

    total = max(len(checks), 1)
    score = max((total - len(failures)) / total, 0.0)

    return EvaluationSummary(
        passed=not failures,
        score=round(score, 2),
        checks=checks,
        failures=failures,
    )


def evaluate_structured_service_output(raw_output: str, validation_error: str | None) -> EvaluationSummary:
    failures: list[str] = []
    checks = ["valid JSON", "schema validation"]

    if validation_error:
        failures.append(validation_error)

    return EvaluationSummary(
        passed=validation_error is None,
        score=1.0 if validation_error is None else 0.0,
        checks=checks,
        failures=failures,
    )
