from unittest.mock import AsyncMock

import pytest

from app.models.ticket_model import PriorityEnum, StatusEnum
from app.service.ticket_service import TicketService


@pytest.mark.asyncio
class TestGetAllTickets:

    @pytest.mark.parametrize(
        "status, priority, repo_result",
        [
            (
                None,
                None,
                [
                    {
                        "title": "Login Issue",
                        "status": StatusEnum.OPEN,
                        "priority": PriorityEnum.HIGH,
                    },
                    {
                        "title": "VPN Issue",
                        "status": StatusEnum.CLOSED,
                        "priority": PriorityEnum.LOW,
                    },
                ],
            ),
            (
                StatusEnum.OPEN,
                None,
                [
                    {
                        "title": "Login Issue",
                        "status": StatusEnum.OPEN,
                        "priority": PriorityEnum.HIGH,
                    }
                ],
            ),
            (
                None,
                PriorityEnum.HIGH,
                [
                    {
                        "title": "Database Error",
                        "status": StatusEnum.IN_PROGRESS,
                        "priority": PriorityEnum.HIGH,
                    }
                ],
            ),
            (
                StatusEnum.OPEN,
                PriorityEnum.HIGH,
                [
                    {
                        "title": "Server Down",
                        "status": StatusEnum.OPEN,
                        "priority": PriorityEnum.HIGH,
                    }
                ],
            ),
        ],
    )
    async def test_get_all_tickets_success(
        self,
        status,
        priority,
        repo_result,
    ):
        repo = AsyncMock()
        repo.get_all.return_value = repo_result

        service = TicketService(repo)

        result = await service.get_all_tickets(
            status=status,
            priority=priority,
        )

        repo.get_all.assert_awaited_once_with(
            status=status,
            priority=priority,
        )

        assert result == repo_result

    @pytest.mark.parametrize(
        "repo_result",
        [
            [],
        ],
    )
    async def test_get_all_tickets_empty(self, repo_result):
        repo = AsyncMock()
        repo.get_all.return_value = repo_result

        service = TicketService(repo)

        result = await service.get_all_tickets()

        repo.get_all.assert_awaited_once_with(
            status=None,
            priority=None,
        )

        assert result == []

    @pytest.mark.parametrize(
        "exception",
        [
            Exception("Database Error"),
            RuntimeError("Unexpected Error"),
        ],
    )
    async def test_get_all_tickets_repository_exception(self, exception):
        repo = AsyncMock()
        repo.get_all.side_effect = exception

        service = TicketService(repo)

        with pytest.raises(type(exception)):
            await service.get_all_tickets()