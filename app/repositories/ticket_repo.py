from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket_model import Ticket
from app.schemas.ticket_schema import TicketSchema, TicketInSchema, TicketUpdateSchema


class TicketRepository:
    def __init__(self,db: AsyncSession):
        self.db = db

    async def create_ticket(self,payload: TicketInSchema):
        ticket = Ticket(**payload.model_dump())
        self.db.add(ticket)
        await self.db.flush()
        await self.db.refresh(ticket)
        return ticket

    async def get_ticket_by_id(self,ticket_id: UUID) -> Ticket| None:
        result = await self.db.execute(
            select(Ticket).where(Ticket.id == ticket_id)
        )

        return result.scalar_one_or_none()

    async def get_ticket_by_title(self, title: str) -> Ticket | None:
        result = await self.db.execute(
            select(Ticket).where(Ticket.title == title)
        )
        return result.scalar_one_or_none()

    async def get_ticket_by_title_exclude_id(self, title: str, exclude_id: UUID) -> Ticket | None:
        result = await self.db.execute(
            select(Ticket).where(Ticket.title == title, Ticket.id != exclude_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self,status:str|None=None,priority:str|None=None):
        query=select(Ticket)
        if status:
            query=query.where(Ticket.status == status)
        if priority:
            query=query.where(Ticket.priority == priority)
        query=query.order_by(Ticket.created_at.desc())
        result=await self.db.execute(query)
        return result.scalars().all()

    async def update_ticket(self,ticket:Ticket,payload: TicketUpdateSchema):
        if payload.title is not None:
            ticket.title = payload.title
        if payload.priority is not None:
            ticket.priority = payload.priority
        if payload.status is not None:
            ticket.status = payload.status
        await self.db.flush()
        await self.db.refresh(ticket)
        return ticket

    async def delete(self, ticket: Ticket):
        await self.db.delete(ticket)
        await self.db.flush()

