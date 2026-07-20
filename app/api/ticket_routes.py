from idlelib import query
from typing import List, Optional

from fastapi import APIRouter, HTTPException,Query

from app.service import ticket_service
from app.service.ticket_service import TicketService
from app.schemas import ticket_schema
router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/ticket", response_model=ticket_schema.TicketOutSchema,status_code=201)
def post_ticket(ticket_in: ticket_schema.TicketInSchema):
    ticket=TicketService.create_ticket(ticket_in)
    return {
        "message":"User Created successfully",
        "ticket": ticket
    }

@router.get("/tickets", response_model=ticket_schema.TicketOutListSchema,status_code=200)
def get_tickets(status:Optional[str]=Query(None),priority:Optional[str]=Query(None)):
    tickets = TicketService.get_all_tickets()
    if status:
        tickets = TicketService.filter_tickets_by_status(status)
    if priority:
        tickets = TicketService.filter_tickets_by_priority(priority)
    return {
        "message":f"All Tickets Retrived successfully and totally of {len(tickets)} tickets ",
        "tickets": tickets
    }
@router.get("/tickets/{id}", response_model=ticket_schema.TicketOutSchema,status_code=200)
def get_ticket_by_id(id:str):
    ticket=TicketService.get_ticket(id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {
        "message":"Ticket retrieved successfully",
        "ticket": ticket
    }

@router.put(path="/tickets/{id}", response_model=ticket_schema.TicketOutSchema,status_code=200)
def edit_ticket(id:str,ticket_in: ticket_schema.TicketUpdateSchema):
    updated_ticket = TicketService.update_ticket(id, ticket_in)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {
        "message": "Ticket updated successfully",
        "ticket": updated_ticket
    }

@router.delete(path="/deleteTicket", status_code=204)
def delete_ticket(id:str):
    ticket = TicketService.delete_ticket(id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {
        "message": "Ticket deleted successfully",
        "ticket": ticket
    }