import pytest
from httpx import AsyncClient

from app.models.ticket_model import PriorityEnum, StatusEnum


@pytest.mark.asyncio
class TestCreateTicket:

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "title": "Login Issue",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.OPEN.value,
            },
            {
                "title": "VPN Issue",
                "priority": PriorityEnum.MEDIUM.value,
                "status": StatusEnum.OPEN.value,
            },
            {
                "title": "Printer Error",
                "priority": PriorityEnum.LOW.value,
                "status": StatusEnum.OPEN.value,
            },
        ],
    )
    #happy
    async def test_create_ticket_success(
        self,
        client: AsyncClient,
        payload,
    ):
        response = await client.post("/tickets/ticket", json=payload)

        assert response.status_code == 201

        data = response.json()["ticket"]

        assert data["title"] == payload["title"]
        assert data["priority"] == payload["priority"]
        assert data["status"] == payload["status"]
        assert "id" in data

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "title": "",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.OPEN.value,
            },
            {
                "title": "   ",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.OPEN.value,
            },
        ],
    )
    #edge
    async def test_create_ticket_invalid_title(
        self,
        client: AsyncClient,
        payload,
    ):
        response = await client.post("/tickets/ticket", json=payload)

        assert response.status_code == 422

   

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "title": "VPN Issue",
                "priority": PriorityEnum.MEDIUM.value,
                "status": StatusEnum.IN_PROGRESS.value,
            },
            {
                "title": "Printer Error",
                "priority": PriorityEnum.LOW.value,
                "status": StatusEnum.CLOSED.value,
            },
            {
                "title": "Database Issue",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.RESOLVED.value,
            },
        ],
    )
    #failure
    async def test_create_ticket_invalid_initial_status(
        self,
        client: AsyncClient,
        payload,
    ):
        response = await client.post("/tickets/ticket", json=payload)
        assert response.status_code == 400