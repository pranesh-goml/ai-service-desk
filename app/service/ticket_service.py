from datetime import datetime
import uuid
from typing import List, Optional

from app.schemas.ticket_schema import TicketInSchema, TicketOutSchema, TicketSchema, TicketUpdateSchema

tickets = {}


class TicketService:
    @staticmethod
    def create_ticket(ticket_data: TicketInSchema) -> TicketSchema:
        ticket = TicketSchema(
            id=str(uuid.uuid4()),
            title=ticket_data.title,
            priority=ticket_data.priority,
            status=ticket_data.status,
            created_at=datetime.now()
        )
        tickets[ticket.id] = ticket
        return ticket
    @staticmethod
    def get_all_tickets() -> List[TicketSchema]:
        return list(tickets.values())
    @staticmethod
    def get_ticket(ticket_id:str) -> Optional[TicketSchema]:
        ticket = tickets.get(ticket_id)
        if not ticket:
            return None
        return ticket
    @staticmethod
    def update_ticket(ticket_id: str,ticket_input:TicketUpdateSchema) -> Optional[TicketSchema]:
        ticket= tickets.get(ticket_id)
        if not ticket:
            return None
        if ticket_input.title is not None:
            ticket.title = ticket_input.title
        if ticket_input.priority is not None:
            ticket.priority = ticket_input.priority
        if ticket_input.status is not None:
            ticket.status = ticket_input.status
        tickets[ticket_id] = ticket
        return ticket
    @staticmethod
    def delete_ticket(ticket_id:str) -> Optional[TicketSchema]:
        ticket= tickets.get(ticket_id)
        if not ticket:
            return None
        tickets.pop(ticket_id)
        return ticket
    @staticmethod
    def filter_tickets_by_priority(priority:str) -> List[TicketSchema]:
        ticket_list = []
        for ticket in tickets.values():
            if ticket.priority.lower() == priority.lower():
                ticket_list.append(ticket)
        return ticket_list
    @staticmethod
    def filter_tickets_by_status(status:str) -> List[TicketSchema]:
        ticket_list = []
        for ticket in tickets.values():
            if ticket.status.lower() == status.lower():
                ticket_list.append(ticket)
        return ticket_list


