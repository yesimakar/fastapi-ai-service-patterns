from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from app.models import GuardrailResult, RiskLevel


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    risk_level: RiskLevel
    required_args: tuple[str, ...]
    handler: Callable[[dict[str, Any]], dict[str, Any]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools = {
            "search_docs": ToolDefinition(
                name="search_docs",
                risk_level=RiskLevel.low,
                required_args=("query",),
                handler=self._search_docs,
            ),
            "create_ticket": ToolDefinition(
                name="create_ticket",
                risk_level=RiskLevel.medium,
                required_args=("title", "summary"),
                handler=self._create_ticket,
            ),
        }

    def list_tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "risk_level": tool.risk_level.value,
                "required_args": list(tool.required_args),
            }
            for tool in self._tools.values()
        ]

    def run(self, tool_name: str, arguments: dict[str, Any]) -> tuple[GuardrailResult, dict[str, Any] | None]:
        tool = self._tools.get(tool_name)
        if tool is None:
            return (
                GuardrailResult(
                    allowed=False,
                    risk_level=RiskLevel.high,
                    reasons=[f"unknown tool: {tool_name}"],
                ),
                None,
            )

        missing = [name for name in tool.required_args if name not in arguments]
        if missing:
            return (
                GuardrailResult(
                    allowed=False,
                    risk_level=tool.risk_level,
                    reasons=[f"missing required arguments: {', '.join(missing)}"],
                ),
                None,
            )

        return GuardrailResult(allowed=True, risk_level=tool.risk_level, reasons=[]), tool.handler(arguments)

    @staticmethod
    def _search_docs(arguments: dict[str, Any]) -> dict[str, Any]:
        return {
            "query": arguments["query"],
            "matches": [
                {"source": "ai-service-patterns.md", "snippet": "Validate model output before returning it to callers."},
                {"source": "reliability.md", "snippet": "Retries and fallbacks should be hidden behind a service boundary."},
            ],
        }

    @staticmethod
    def _create_ticket(arguments: dict[str, Any]) -> dict[str, Any]:
        return {
            "ticket_id": "ticket_demo_001",
            "title": arguments["title"],
            "status": "created",
        }
