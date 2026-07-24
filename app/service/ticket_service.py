from datetime import datetime
import uuid
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException

from app.models.ticket_model import StatusEnum
from app.repositories.ticket_repo import TicketRepository
from app.schemas.ticket_schema import TicketInSchema
from app.core.exceptions import ClosedTicketError, DuplicateTicketError
from app.service.aws.bedrock_service import BedrockService

class TicketService:
    def __init__(self, repo: TicketRepository):
        self.repo = repo

    async def create_ticket(self,ticket_input:TicketInSchema):
        existing = await self.repo.get_ticket_by_title(ticket_input.title)
        if existing is not None:
            raise DuplicateTicketError("Ticket with this title already exists")
        if ticket_input.status != StatusEnum.OPEN:
            raise HTTPException(status_code=400,detail="A Ticket can be raised only as a Open ticket.")
        bedrock = BedrockService()
        description = bedrock.generate_description(ticket_input)
        return await self.repo.create_ticket(ticket_input,description)

    async def get_all_tickets(self, status=None, priority=None):
        return await self.repo.get_all(status=status, priority=priority)

    async def get_ticket(self, ticket_id):
        ticket = await self.repo.get_ticket_by_id(ticket_id)
        if ticket is None:
            return None
        return ticket

    async def update_ticket(self,ticket_id,ticket_input) :
        ticket = await self.repo.get_ticket_by_id(ticket_id)
        if ticket is None:
            return None
        if ticket.status == StatusEnum.CLOSED:
            raise ClosedTicketError("Cannot update closed ticket")
        if ticket_input.title is not None:
            existing = await self.repo.get_ticket_by_title_exclude_id(ticket_input.title, ticket_id)
            if existing is not None:
                raise DuplicateTicketError("Ticket with this title already exists")
        return await self.repo.update_ticket(ticket,ticket_input)

    async def delete_ticket(self,ticket_id:UUID) :
        ticket = await self.repo.get_ticket_by_id(ticket_id)
        if ticket is None:
            return None
        await self.repo.delete(ticket)
        return ticket
