import pytest
from httpx import AsyncClient

from app.models.ticket_model import PriorityEnum, StatusEnum


@pytest.mark.asyncio
class TestGetTicket:

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
                "status": StatusEnum.IN_PROGRESS.value,
            },
        ],
    )
    async def test_get_ticket_success(
        self,
        client: AsyncClient,
        payload,
    ):
        create_payload = payload.copy()
        create_payload["status"] = StatusEnum.OPEN.value
        create = await client.post("/tickets/ticket", json=create_payload)

        assert create.status_code == 201

        ticket = create.json()["ticket"]

        if payload["status"] != StatusEnum.OPEN.value:
            update = await client.put(
                f"/tickets/ticket/{ticket['id']}",
                json=payload
            )
            assert update.status_code == 200
            ticket = update.json()["ticket"]

        response = await client.get(f"/tickets/ticket/{ticket['id']}")

        assert response.status_code == 200

        data = response.json()["ticket"]

        assert data["id"] == ticket["id"]
        assert data["title"] == payload["title"]
        assert data["priority"] == payload["priority"]
        assert data["status"] == payload["status"]

    @pytest.mark.parametrize(
        "ticket_id",
        [
            "11111111-1111-1111-1111-111111111111",
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        ],
    )
    async def test_get_ticket_not_found(
        self,
        client: AsyncClient,
        ticket_id,
    ):
        response = await client.get(f"/tickets/ticket/{ticket_id}")

        assert response.status_code == 404

    @pytest.mark.parametrize(
        "ticket_id",
        [
            "abc",
            "123",
            "invalid-uuid",
            "",
        ],
    )
    async def test_get_ticket_invalid_uuid(
        self,
        client: AsyncClient,
        ticket_id,
    ):
        response = await client.get(f"/tickets/ticket/{ticket_id}")

        assert response.status_code == 422

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "title": "Schema Test",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.OPEN.value,
            },
        ],
    )
    async def test_get_ticket_response_schema(
        self,
        client: AsyncClient,
        payload,
    ):
        create = await client.post("/tickets/ticket", json=payload)

        ticket = create.json()["ticket"]

        response = await client.get(f"/tickets/ticket/{ticket['id']}")

        data = response.json()["ticket"]

        expected_fields = {
            "id",
            "title",
            "priority",
            "status",
            "created_at",
            "updated_at",
        }

        assert expected_fields.issubset(data.keys())