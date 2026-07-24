import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.repositories.ticket_repo import TicketRepository
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
async def summarize_ticket(
    payload: SummarizeRequest,
    service: BedrockService = Depends(get_bedrock_service),
    db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    try:
        # Fetch the ticket list from repository
        try:
            ticket_repo = TicketRepository(db)
            tickets = await ticket_repo.get_all()
            
            # Format the tickets list nicely
            ticket_list_str = "\n".join([
                f"- Title: {t.title}, Priority: {t.priority.value if hasattr(t.priority, 'value') else t.priority}, Status: {t.status.value if hasattr(t.status, 'value') else t.status}, Description: {t.description}"
                for t in tickets
            ])
        except Exception as db_exc:
            print(f"Warning: Database query failed (PostgreSQL might be offline): {db_exc}")
            ticket_list_str = "(No existing tickets available. Database is offline/unreachable.)"
        
        return service.summarize_ticket(payload.ticket_description, ticket_list=ticket_list_str)
    except BedrockServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI service is temporarily unavailable",
        ) from exc

