from app.services.tool_registry import ToolRegistry


def test_unknown_tool_is_blocked():
    registry = ToolRegistry()
    guardrail, result = registry.run("delete_database", {})

    assert guardrail.allowed is False
    assert result is None


def test_missing_required_argument_is_blocked():
    registry = ToolRegistry()
    guardrail, result = registry.run("create_ticket", {"title": "Missing summary"})

    assert guardrail.allowed is False
    assert result is None
