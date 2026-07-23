import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, String, DateTime, UUID, Enum, func

from app.core.database import Base

class PriorityEnum(str, PyEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class StatusEnum(str, PyEnum):
    OPEN = "Open"
    IN_PROGRESS = "In-Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
class Ticket(Base):
    __tablename__ = "ticket"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    priority = Column(Enum(PriorityEnum,name="priority_enum"), nullable=False)
    status = Column(Enum(StatusEnum,name="status_enum"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
