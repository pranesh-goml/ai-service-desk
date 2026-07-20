import uuid
from datetime import datetime
class Ticket:
    __tablename__ = "ticket"
    id : str
    title : str
    priority : str
    status : str
    created_at : datetime