from datetime import datetime
from typing import Optional, List, Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from app.models.ticket_model import PriorityEnum, StatusEnum
from app.service.validation_service import strip_whitespace, strip_whitespace_and_validate

class TicketInSchema(BaseModel):
    title: str= Field(...,min_length=1,description="Title of the ticket")
    priority: PriorityEnum
    status: StatusEnum

    @field_validator("title", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return strip_whitespace(v)

    class Config:
        extra = "forbid"

class TicketSchema(BaseModel):
    id: UUID
    title: str
    priority: str
    status: str
    description: str
    created_at: datetime
    updated_at: datetime

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

    @field_validator("title", mode="before")
    @classmethod
    def strip_whitespace_and_validate(cls, v: Optional[str]) -> Optional[str]:
        return strip_whitespace_and_validate(v)

    class Config:
        extra = "forbid"


class SummarizeRequest(BaseModel):
    ticket_description: str = Field(min_length=10, max_length=5_000)


class SummarizeResponse(BaseModel):
    summary: str
    suggested_response: str