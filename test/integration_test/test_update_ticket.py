import pytest
from httpx import AsyncClient

from app.models.ticket_model import PriorityEnum, StatusEnum


@pytest.mark.asyncio
class TestUpdateTicket:

    @pytest.mark.parametrize(
        "create_payload, update_payload",
        [
            (
                {
                    "title": "Login Issue",
                    "priority": PriorityEnum.HIGH.value,
                    "status": StatusEnum.OPEN.value,
                },
                {
                    "title": "Updated Login Issue",
                    "priority": PriorityEnum.MEDIUM.value,
                    "status": StatusEnum.IN_PROGRESS.value,
                },
            ),
            (
                {
                    "title": "VPN Issue",
                    "priority": PriorityEnum.LOW.value,
                    "status": StatusEnum.OPEN.value,
                },
                {
                    "title": "Updated VPN Issue",
                    "priority": PriorityEnum.HIGH.value,
                    "status": StatusEnum.RESOLVED.value,
                },
            ),
        ],
    )
    async def test_update_ticket_success(
        self,
        client: AsyncClient,
        create_payload,
        update_payload,
    ):
        create = await client.post("/tickets/ticket", json=create_payload)

        assert create.status_code == 201

        ticket = create.json()["ticket"]

        response = await client.put(
            f"/tickets/ticket/{ticket['id']}",
            json=update_payload,
        )

        assert response.status_code == 200

        data = response.json()["ticket"]

        assert data["title"] == update_payload["title"]
        assert data["priority"] == update_payload["priority"]
        assert data["status"] == update_payload["status"]

    @pytest.mark.parametrize(
        "ticket_id",
        [
            "11111111-1111-1111-1111-111111111111",
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        ],
    )
    async def test_update_ticket_not_found(
        self,
        client: AsyncClient,
        ticket_id,
    ):
        payload = {
            "title": "Updated",
            "priority": PriorityEnum.HIGH.value,
            "status": StatusEnum.OPEN.value,
        }

        response = await client.put(
            f"/tickets/ticket/{ticket_id}",
            json=payload,
        )

        assert response.status_code == 404

    @pytest.mark.parametrize(
        "ticket_id",
        [
            "abc",
            "123",
            "invalid-uuid",
        ],
    )
    async def test_update_ticket_invalid_uuid(
        self,
        client: AsyncClient,
        ticket_id,
    ):
        payload = {
            "title": "Updated",
            "priority": PriorityEnum.HIGH.value,
            "status": StatusEnum.OPEN.value,
        }

        response = await client.put(
            f"/tickets/ticket/{ticket_id}",
            json=payload,
        )

        assert response.status_code == 422

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
    async def test_update_ticket_invalid_title(
        self,
        client: AsyncClient,
        payload,
    ):
        create = await client.post(
            "/tickets/ticket",
            json={
                "title": "Original Ticket",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.OPEN.value,
            },
        )

        ticket = create.json()["ticket"]

        response = await client.put(
            f"/tickets/ticket/{ticket['id']}",
            json=payload,
        )

        assert response.status_code == 422

    @pytest.mark.parametrize(
        "closed_ticket",
        [
            {
                "title": "Closed Ticket",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.CLOSED.value,
            }
        ],
    )
    async def test_update_closed_ticket(
        self,
        client: AsyncClient,
        closed_ticket,
    ):
        create = await client.post(
            "/tickets/ticket",
            json=closed_ticket,
        )

        ticket = create.json()["ticket"]

        response = await client.put(
            f"/tickets/ticket/{ticket['id']}",
            json={
                "title": "Cannot Update",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.OPEN.value,
            },
        )

        assert response.status_code == 400

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "title": "Duplicate Ticket",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.OPEN.value,
            }
        ],
    )
    async def test_update_duplicate_title(
        self,
        client: AsyncClient,
        payload,
    ):
        first = await client.post("/tickets/ticket", json=payload)
        second = await client.post(
            "/tickets/ticket",
            json={
                "title": "Another Ticket",
                "priority": PriorityEnum.LOW.value,
                "status": StatusEnum.OPEN.value,
            },
        )

        first_ticket = first.json()["ticket"]
        second_ticket = second.json()["ticket"]

        response = await client.put(
            f"/tickets/ticket/{second_ticket['id']}",
            json={
                "title": payload["title"],
                "priority": PriorityEnum.LOW.value,
                "status": StatusEnum.OPEN.value,
            },
        )

        assert response.status_code == 409