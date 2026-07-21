from datetime import datetime
from typing import Optional, List, Literal
from uuid import UUID

from pydantic import BaseModel,Field
from app.models.ticket_model import PriorityEnum, StatusEnum
class TicketInSchema(BaseModel):
    title: str
    priority: PriorityEnum
    status: StatusEnum
    class Config:
        extra = "forbid"

class TicketSchema(BaseModel):
    id: UUID
    title: str
    priority: str
    status: str
    created_at: datetime

class TicketOutSchema(BaseModel):
    message: Optional[str]
    ticket: TicketSchema

class TicketOutListSchema(BaseModel):
    message: Optional[str]
    tickets: List[TicketSchema]

class TicketUpdateSchema(BaseModel):
    title: Optional[str]
    priority: Optional[PriorityEnum]
    status: Optional[StatusEnum]
    class Config:
        extra = "forbid"
