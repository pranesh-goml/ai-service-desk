import uuid
from unittest.mock import AsyncMock

import pytest

from app.models.ticket_model import PriorityEnum, StatusEnum
from app.schemas.ticket_schema import TicketUpdateSchema
from app.service.ticket_service import TicketService


@pytest.mark.asyncio
class TestUpdateTicket:

    @pytest.mark.parametrize(
        "payload",
        [
            TicketUpdateSchema(
                title="Updated Login Issue",
                priority=PriorityEnum.HIGH,
                status=StatusEnum.IN_PROGRESS,
            ),
            TicketUpdateSchema(
                title="Updated VPN Issue",
                priority=PriorityEnum.MEDIUM,
                status=StatusEnum.RESOLVED,
            ),
            TicketUpdateSchema(
                title="Updated Printer Issue",
                priority=PriorityEnum.LOW,
                status=StatusEnum.OPEN,
            ),
        ],
    )
    async def test_update_ticket_success(self, payload):
        ticket_id = uuid.uuid4()

        repo = AsyncMock()
        mock_ticket = AsyncMock()
        mock_ticket.status = StatusEnum.OPEN
        repo.get_ticket_by_id.return_value = mock_ticket
        repo.update_ticket.return_value = payload

        service = TicketService(repo)

        result = await service.update_ticket(ticket_id, payload)

        repo.get_ticket_by_id.assert_awaited_once_with(ticket_id)
        repo.update_ticket.assert_awaited_once_with(mock_ticket, payload)
        assert result == payload

    @pytest.mark.parametrize(
        "repo_result",
        [
            None,
        ],
    )
    async def test_update_ticket_not_found(self, repo_result):
        ticket_id = uuid.uuid4()

        payload = TicketUpdateSchema(
            title="Does Not Exist",
            priority=PriorityEnum.HIGH,
            status=StatusEnum.OPEN,
        )

        repo = AsyncMock()
        repo.get_ticket_by_id.return_value = None

        service = TicketService(repo)

        result = await service.update_ticket(ticket_id, payload)

        repo.get_ticket_by_id.assert_awaited_once_with(ticket_id)
        repo.update_ticket.assert_not_called()
        assert result is None

    @pytest.mark.parametrize(
        "exception",
        [
            Exception("Database Error"),
            RuntimeError("Unexpected Error"),
        ],
    )
    async def test_update_ticket_repository_exception(self, exception):
        ticket_id = uuid.uuid4()

        payload = TicketUpdateSchema(
            title="Update Failure",
            priority=PriorityEnum.HIGH,
            status=StatusEnum.OPEN,
        )

        repo = AsyncMock()
        repo.update_ticket.side_effect = exception

        service = TicketService(repo)

        with pytest.raises(type(exception)):
            await service.update_ticket(ticket_id, payload)