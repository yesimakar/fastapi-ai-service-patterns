from __future__ import annotations

from fastapi import APIRouter, Request

from app.models import ToolCallRequest, ToolCallResponse
from app.services.tool_registry import ToolRegistry

router = APIRouter(prefix="/v1", tags=["tools"])


@router.get("/tools")
async def list_tools(request: Request) -> list[dict]:
    registry: ToolRegistry = request.app.state.tool_registry
    return registry.list_tools()


@router.post("/tools/run", response_model=ToolCallResponse)
async def run_tool(request: Request, payload: ToolCallRequest) -> ToolCallResponse:
    registry: ToolRegistry = request.app.state.tool_registry
    guardrail, result = registry.run(payload.tool_name, payload.arguments)
    return ToolCallResponse(
        request_id=request.state.request_id,
        tool_name=payload.tool_name,
        allowed=guardrail.allowed,
        risk_level=guardrail.risk_level,
        result=result,
        reasons=guardrail.reasons,
    )
