from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.models import StreamRequest
from app.providers.base import LLMProvider, LLMRequest

router = APIRouter(prefix="/v1", tags=["streaming"])


@router.post("/stream")
async def stream_response(request: Request, payload: StreamRequest) -> StreamingResponse:
    provider: LLMProvider = request.app.state.provider
    llm_request = LLMRequest(prompt=payload.prompt, context=payload.context)

    async def token_stream():
        async for token in provider.stream(llm_request):
            yield token

    return StreamingResponse(token_stream(), media_type="text/plain")
