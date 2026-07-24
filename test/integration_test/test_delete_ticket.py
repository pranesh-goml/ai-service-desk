import pytest
from httpx import AsyncClient

from app.models.ticket_model import PriorityEnum, StatusEnum


@pytest.mark.asyncio
class TestDeleteTicket:

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "title": "Delete Login Issue",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.OPEN.value,
            },
            {
                "title": "Delete VPN Issue",
                "priority": PriorityEnum.MEDIUM.value,
                "status": StatusEnum.IN_PROGRESS.value,
            },
        ],
    )
    #happy
    async def test_delete_ticket_success(
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

        response = await client.delete(f"/tickets/ticket/{ticket['id']}")

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "ticket_id",
        [
            "11111111-1111-1111-1111-111111111111",
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        ],
    )
    #edge
    async def test_delete_ticket_not_found(
        self,
        client: AsyncClient,
        ticket_id,
    ):
        response = await client.delete(f"/tickets/ticket/{ticket_id}")

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
    #failure
    async def test_delete_ticket_invalid_uuid(
        self,
        client: AsyncClient,
        ticket_id,
    ):
        response = await client.delete(f"/tickets/ticket/{ticket_id}")

        assert response.status_code == 422

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "title": "Delete Verification",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.OPEN.value,
            }
        ],
    )
    #edge
    async def test_deleted_ticket_cannot_be_fetched(
        self,
        client: AsyncClient,
        payload,
    ):
        create = await client.post("/tickets/ticket", json=payload)

        ticket = create.json()["ticket"]

        delete = await client.delete(f"/tickets/ticket/{ticket['id']}")

        assert delete.status_code == 200

        response = await client.get(f"/tickets/ticket/{ticket['id']}")

        assert response.status_code == 404

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "title": "Delete Twice",
                "priority": PriorityEnum.HIGH.value,
                "status": StatusEnum.OPEN.value,
            }
        ],
    )
    #edge
    async def test_delete_ticket_twice(
        self,
        client: AsyncClient,
        payload,
    ):
        create = await client.post("/tickets/ticket", json=payload)

        ticket = create.json()["ticket"]

        first = await client.delete(f"/tickets/ticket/{ticket['id']}")

        assert first.status_code == 200

        second = await client.delete(f"/tickets/ticket/{ticket['id']}")

        assert second.status_code == 404