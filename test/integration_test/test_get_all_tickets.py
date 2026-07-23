import pytest
from httpx import AsyncClient

from app.models.ticket_model import PriorityEnum, StatusEnum


@pytest.mark.asyncio
class TestGetAllTickets:

    @pytest.mark.parametrize(
        "tickets",
        [
            [
                {
                    "title": "Login Issue",
                    "priority": PriorityEnum.HIGH.value,
                    "status": StatusEnum.OPEN.value,
                },
                {
                    "title": "VPN Issue",
                    "priority": PriorityEnum.LOW.value,
                    "status": StatusEnum.RESOLVED.value,
                },
                {
                    "title": "Printer Error",
                    "priority": PriorityEnum.MEDIUM.value,
                    "status": StatusEnum.IN_PROGRESS.value,
                },
            ]
        ],
    )
    async def test_get_all_tickets(
        self,
        client: AsyncClient,
        tickets,
    ):
        for ticket in tickets:
            response = await client.post("/tickets/ticket", json=ticket)
            assert response.status_code == 201

        response = await client.get("/tickets/ticket")

        assert response.status_code == 200

        data = response.json()["tickets"]

        assert isinstance(data, list)
        assert len(data) >= len(tickets)

    async def test_get_all_tickets_empty(
        self,
        client: AsyncClient,
    ):
        response = await client.get("/tickets/ticket")

        assert response.status_code == 200
        assert isinstance(response.json()["tickets"], list)

    @pytest.mark.parametrize(
        "status",
        [
            StatusEnum.OPEN.value,
            StatusEnum.IN_PROGRESS.value,
            StatusEnum.RESOLVED.value,
        ],
    )
    async def test_filter_by_status(
        self,
        client: AsyncClient,
        status,
    ):
        response = await client.get(
            f"/tickets/ticket?status={status}"
        )

        assert response.status_code == 200

        for ticket in response.json()["tickets"]:
            assert ticket["status"] == status

    @pytest.mark.parametrize(
        "priority",
        [
            PriorityEnum.HIGH.value,
            PriorityEnum.MEDIUM.value,
            PriorityEnum.LOW.value,
        ],
    )
    async def test_filter_by_priority(
        self,
        client: AsyncClient,
        priority,
    ):
        response = await client.get(
            f"/tickets/ticket?priority={priority}"
        )

        assert response.status_code == 200

        for ticket in response.json()["tickets"]:
            assert ticket["priority"] == priority

    @pytest.mark.parametrize(
        "status, priority",
        [
            (
                StatusEnum.OPEN.value,
                PriorityEnum.HIGH.value,
            ),
            (
                StatusEnum.IN_PROGRESS.value,
                PriorityEnum.MEDIUM.value,
            ),
            (
                StatusEnum.RESOLVED.value,
                PriorityEnum.LOW.value,
            ),
        ],
    )
    async def test_filter_by_status_and_priority(
        self,
        client: AsyncClient,
        status,
        priority,
    ):
        response = await client.get(
            f"/tickets/ticket?status={status}&priority={priority}"
        )

        assert response.status_code == 200

        for ticket in response.json()["tickets"]:
            assert ticket["status"] == status
            assert ticket["priority"] == priority

    @pytest.mark.parametrize(
        "status",
        [
            "invalid",
            "done",
            "completed",
        ],
    )
    async def test_invalid_status_filter(
        self,
        client: AsyncClient,
        status,
    ):
        response = await client.get(
            f"/tickets/ticket?status={status}"
        )

        assert response.status_code == 422

    @pytest.mark.parametrize(
        "priority",
        [
            "urgent",
            "highest",
            "unknown",
        ],
    )
    async def test_invalid_priority_filter(
        self,
        client: AsyncClient,
        priority,
    ):
        response = await client.get(
            f"/tickets/ticket?priority={priority}"
        )

        assert response.status_code == 422