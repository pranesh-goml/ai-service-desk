import uuid
from unittest.mock import AsyncMock

import pytest

from app.service.ticket_service import TicketService


@pytest.mark.asyncio
class TestDeleteTicket:

    @pytest.mark.parametrize(
        "repo_result",
        [
            True,
            {"message": "Ticket deleted successfully"},
        ],
    )
    async def test_delete_ticket_success(self, repo_result):
        ticket_id = uuid.uuid4()

        repo = AsyncMock()
        mock_ticket = AsyncMock()
        repo.get_ticket_by_id.return_value = mock_ticket

        service = TicketService(repo)

        result = await service.delete_ticket(ticket_id)

        repo.get_ticket_by_id.assert_awaited_once_with(ticket_id)
        repo.delete.assert_awaited_once_with(mock_ticket)
        assert result == mock_ticket

    @pytest.mark.parametrize(
        "repo_result",
        [
            None,
            False,
        ],
    )
    async def test_delete_ticket_not_found(self, repo_result):
        ticket_id = uuid.uuid4()

        repo = AsyncMock()
        repo.get_ticket_by_id.return_value = None

        service = TicketService(repo)

        result = await service.delete_ticket(ticket_id)

        repo.get_ticket_by_id.assert_awaited_once_with(ticket_id)
        repo.delete.assert_not_called()
        assert result is None

    @pytest.mark.parametrize(
        "exception",
        [
            Exception("Database Error"),
            RuntimeError("Unexpected Error"),
        ],
    )
    async def test_delete_ticket_repository_exception(self, exception):
        ticket_id = uuid.uuid4()

        repo = AsyncMock()
        repo.get_ticket_by_id.side_effect = exception

        service = TicketService(repo)

        with pytest.raises(type(exception)):
            await service.delete_ticket(ticket_id)