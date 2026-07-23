import pytest
from unittest.mock import AsyncMock

from app.models.ticket_model import PriorityEnum, StatusEnum
from app.schemas.ticket_schema import TicketInSchema
from app.service.ticket_service import TicketService


@pytest.mark.asyncio
class TestCreateTicket:

    @pytest.mark.parametrize(
        "payload",
        [
            TicketInSchema(
                title="Login Issue",
                priority=PriorityEnum.HIGH,
                status=StatusEnum.OPEN,
            ),
            TicketInSchema(
                title="Printer Error",
                priority=PriorityEnum.MEDIUM,
                status=StatusEnum.IN_PROGRESS,
            ),
            TicketInSchema(
                title="VPN Issue",
                priority=PriorityEnum.LOW,
                status=StatusEnum.CLOSED,
            ),
        ],
    )
    async def test_create_ticket_success(self, payload):
        repo = AsyncMock()

        repo.create_ticket.return_value = payload

        service = TicketService(repo)

        result = await service.create_ticket(payload)

        repo.create_ticket.assert_awaited_once_with(payload)
        assert result == payload

    @pytest.mark.parametrize(
        "exception",
        [
            Exception("Database Error"),
            RuntimeError("Unexpected Error"),
        ],
    )
    async def test_create_ticket_exception(self, exception):
        payload = TicketInSchema(
            title="Laptop Issue",
            priority=PriorityEnum.HIGH,
            status=StatusEnum.OPEN,
        )

        repo = AsyncMock()
        repo.create_ticket.side_effect = exception

        service = TicketService(repo)

        with pytest.raises(type(exception)):
            await service.create_ticket(payload)