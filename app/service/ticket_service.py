from datetime import datetime
import uuid
from typing import List, Optional
from uuid import UUID

from app.models.ticket_model import StatusEnum
from app.repositories.ticket_repo import TicketRepository
from app.schemas.ticket_schema import TicketInSchema



class TicketService:
    def __init__(self, repo: TicketRepository):
        self.repo = repo

    async def create_ticket(self,ticket_input:TicketInSchema):
        return await self.repo.create_ticket(ticket_input)

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
            return None
        return await self.repo.update_ticket(ticket,ticket_input)

    async def delete_ticket(self,ticket_id:UUID) :
        ticket = await self.repo.get_ticket_by_id(ticket_id)
        if ticket is None:
            return None
        await self.repo.delete(ticket)
        return ticket
