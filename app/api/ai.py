import os
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.ticket_schema import SummarizeRequest, SummarizeResponse
from app.service.aws.bedrock_service import (
    BedrockService,
    BedrockServiceError,
    FakeBedrockService,
)

router = APIRouter(prefix="/ai", tags=["AI"])

def get_bedrock_service() -> BedrockService:
    return BedrockService()

@router.post("/summarize", response_model=SummarizeResponse)
def summarize_ticket(
    payload: SummarizeRequest,
    service: BedrockService = Depends(get_bedrock_service),
) -> dict[str, str]:
    try:
        return service.summarize_ticket(payload.ticket_description)
    except BedrockServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI service is temporarily unavailable",
        ) from exc

