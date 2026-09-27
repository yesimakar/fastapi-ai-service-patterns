from app.services.evaluation import evaluate_output


def test_evaluation_passes_required_and_forbidden_terms():
    result = evaluate_output(
        output="The response includes validation and fallback handling.",
        required_terms=["validation", "fallback"],
        forbidden_terms=["secret"],
    )

    assert result.passed is True
    assert result.score == 1.0


def test_evaluation_fails_for_missing_required_term():
    result = evaluate_output(
        output="The response includes validation.",
        required_terms=["observability"],
    )

    assert result.passed is False
    assert result.score == 0.0
