from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

class TicketInSchema(BaseModel):
    title : str
    priority : str
    status : str
class TicketSchema(BaseModel):
    id : str
    title : str
    priority : str
    status : str
    created_at : datetime
class TicketOutSchema(BaseModel):
    message : Optional[str]
    ticket : TicketSchema
class TicketOutListSchema(BaseModel):
    message : Optional[str]
    tickets : List[TicketSchema]
class TicketUpdateSchema(BaseModel):
    title : Optional[str]
    priority : Optional[str]
    status : Optional[str]
