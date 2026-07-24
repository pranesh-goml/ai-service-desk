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

        ],
    )
    #happy
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
    #edge
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
    #failure
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

        ],
    )
    #edge
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
    #edge
    async def test_update_closed_ticket(
        self,
        client: AsyncClient,
        closed_ticket,
    ):
        create_payload = closed_ticket.copy()
        create_payload["status"] = StatusEnum.OPEN.value
        create = await client.post(
            "/tickets/ticket",
            json=create_payload,
        )

        ticket = create.json()["ticket"]

        update_closed = await client.put(
            f"/tickets/ticket/{ticket['id']}",
            json=closed_ticket
        )
        assert update_closed.status_code == 200

        response = await client.put(
            f"/tickets/ticket/{ticket['id']}",
            json={
                "title": "Cannot Update",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.OPEN.value,
            },
        )

        assert response.status_code == 400
