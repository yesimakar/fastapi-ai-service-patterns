from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class SchemaName(str, Enum):
    support_ticket = "support_ticket"
    action_plan = "action_plan"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class GuardrailResult(BaseModel):
    allowed: bool
    risk_level: RiskLevel
    reasons: list[str] = Field(default_factory=list)


class StructuredGenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    schema_name: SchemaName = SchemaName.support_ticket
    context: list[str] = Field(default_factory=list, max_length=10)
    enable_evaluation: bool = True


class SupportTicket(BaseModel):
    title: str = Field(min_length=3)
    summary: str = Field(min_length=10)
    priority: Literal["low", "medium", "high"]
    next_action: str = Field(min_length=5)


class ActionPlan(BaseModel):
    goal: str = Field(min_length=3)
    steps: list[str] = Field(min_length=1)
    risk: Literal["low", "medium", "high"]
    owner: str = Field(min_length=2)


class EvaluationSummary(BaseModel):
    passed: bool
    score: float
    checks: list[str]
    failures: list[str] = Field(default_factory=list)


class StructuredGenerateResponse(BaseModel):
    request_id: str
    provider: str
    model: str
    schema_name: SchemaName
    raw_output: str
    parsed_output: dict[str, Any] | None
    validation_error: str | None
    guardrail: GuardrailResult
    evaluation: EvaluationSummary | None = None


class StreamRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    context: list[str] = Field(default_factory=list, max_length=10)


class GuardrailCheckRequest(BaseModel):
    text: str = Field(min_length=1, max_length=6000)


class ToolCallRequest(BaseModel):
    tool_name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolCallResponse(BaseModel):
    request_id: str
    tool_name: str
    allowed: bool
    risk_level: RiskLevel
    result: dict[str, Any] | None
    reasons: list[str]


class EvaluationRequest(BaseModel):
    prompt: str = Field(min_length=1)
    output: str = Field(min_length=1)
    required_terms: list[str] = Field(default_factory=list)
    forbidden_terms: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    service: str
    status: str
    version: str
