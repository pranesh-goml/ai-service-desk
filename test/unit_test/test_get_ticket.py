import uuid
from unittest.mock import AsyncMock

import pytest

from app.service.ticket_service import TicketService


@pytest.mark.asyncio
class TestGetTicket:

    @pytest.mark.parametrize(
        "repo_result",
        [
            {
                "id": uuid.uuid4(),
                "title": "Login Issue",
                "priority": "High",
                "status": "Open",
            },
            {
                "id": uuid.uuid4(),
                "title": "VPN Issue",
                "priority": "Medium",
                "status": "In-Progress",
            },
        ],
    )
    async def test_get_ticket_success(self, repo_result):
        repo = AsyncMock()
        repo.get_ticket_by_id.return_value = repo_result

        service = TicketService(repo)

        ticket_id = uuid.uuid4()

        result = await service.get_ticket(ticket_id)

        repo.get_ticket_by_id.assert_awaited_once_with(ticket_id)
        assert result == repo_result

    @pytest.mark.parametrize(
        "repo_result",
        [
            None,
        ],
    )
    async def test_get_ticket_not_found(self, repo_result):
        repo = AsyncMock()
        repo.get_ticket_by_id.return_value = repo_result

        service = TicketService(repo)

        ticket_id = uuid.uuid4()

        result = await service.get_ticket(ticket_id)

        repo.get_ticket_by_id.assert_awaited_once_with(ticket_id)
        assert result is None

    @pytest.mark.parametrize(
        "exception",
        [
            Exception("Database Error"),
            RuntimeError("Unexpected Error"),
        ],
    )
    async def test_get_ticket_repository_exception(self, exception):
        repo = AsyncMock()
        repo.get_ticket_by_id.side_effect = exception

        service = TicketService(repo)

        with pytest.raises(type(exception)):
            await service.get_ticket(uuid.uuid4())