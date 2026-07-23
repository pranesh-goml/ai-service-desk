class DuplicateTicketError(Exception):
    """Raised when a ticket with the same title already exists."""
    pass


class ClosedTicketError(Exception):
    """Raised when an operation is performed on a closed ticket."""
    pass
