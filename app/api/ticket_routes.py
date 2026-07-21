from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.repositories.ticket_repo import TicketRepository
from app.service.ticket_service import TicketService
from app.schemas import ticket_schema
from app.models.ticket_model import PriorityEnum, StatusEnum

router = APIRouter(prefix="/tickets", tags=["ticket"])

@router.post("/ticket", response_model=ticket_schema.TicketOutSchema,status_code=201)
async def post_ticket(ticket_in: ticket_schema.TicketInSchema,db:AsyncSession=Depends(get_db)):

    service=TicketService(TicketRepository(db))
    ticket=await service.create_ticket(ticket_in)
    return {
        "message":"User Created successfully",
        "ticket": ticket
    }

@router.get("/ticket",response_model=ticket_schema.TicketOutListSchema,status_code=200)
async def get_tickets(status: Optional[StatusEnum] = Query(None),priority: Optional[PriorityEnum] = Query(None),db: AsyncSession = Depends(get_db)):
    service = TicketService(TicketRepository(db))
    tickets = await service.get_all_tickets(status=status,priority=priority)
    return {
        "message": f"Retrieved {len(tickets)} ticket(s) successfully",
        "tickets": tickets
    }

@router.get("/ticket/{id}",response_model=ticket_schema.TicketOutSchema,status_code=200)
async def get_ticket_by_id(id: UUID,db: AsyncSession = Depends(get_db)):
    service = TicketService(TicketRepository(db))
    ticket = await service.get_ticket(id)
    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )
    return {
        "message": "Ticket retrieved successfully",
        "ticket": ticket
    }

@router.put("/ticket/{id}",response_model=ticket_schema.TicketOutSchema,status_code=200)
async def edit_ticket(id: UUID,ticket_in: ticket_schema.TicketUpdateSchema,db: AsyncSession = Depends(get_db)):
    service = TicketService(TicketRepository(db))
    updated_ticket = await service.update_ticket(
        id,
        ticket_in
    )
    if updated_ticket is None:
        raise HTTPException(status_code=404,detail="Ticket not found")
    return {
        "message": "Ticket updated successfully",
        "ticket": updated_ticket
    }


@router.delete("/ticket/{id}",status_code=200)
async def delete_ticket(id: UUID,db: AsyncSession = Depends(get_db)):
    service = TicketService(TicketRepository(db))
    deleted_ticket = await service.delete_ticket(id)
    if deleted_ticket is None:
        raise HTTPException(status_code=404,detail="Ticket not found")
    return {
        "message": "Ticket deleted successfully",
        "ticket": deleted_ticket
    }