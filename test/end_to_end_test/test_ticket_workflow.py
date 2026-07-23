import pytest
from httpx import AsyncClient

from app.models.ticket_model import PriorityEnum, StatusEnum


@pytest.mark.asyncio
class TestTicketWorkflow:

    @pytest.mark.parametrize(
        "create_payload, update_payload",
        [
            (
                {
                    "title": "E2E Login Issue",
                    "priority": PriorityEnum.HIGH.value,
                    "status": StatusEnum.OPEN.value,
                },
                {
                    "title": "E2E Login Issue Updated",
                    "priority": PriorityEnum.MEDIUM.value,
                    "status": StatusEnum.IN_PROGRESS.value,
                },
            ),
            (
                {
                    "title": "E2E VPN Issue",
                    "priority": PriorityEnum.LOW.value,
                    "status": StatusEnum.OPEN.value,
                },
                {
                    "title": "E2E VPN Issue Updated",
                    "priority": PriorityEnum.HIGH.value,
                    "status": StatusEnum.RESOLVED.value,
                },
            ),
        ],
    )
    async def test_ticket_complete_workflow(
        self,
        client: AsyncClient,
        create_payload,
        update_payload,
    ):
        # ----------------------------
        # Create Ticket
        # ----------------------------
        create_response = await client.post(
            "/tickets/ticket",
            json=create_payload,
        )

        assert create_response.status_code == 201

        created_ticket = create_response.json()["ticket"]

        ticket_id = created_ticket["id"]

        assert created_ticket["title"] == create_payload["title"]
        assert created_ticket["priority"] == create_payload["priority"]
        assert created_ticket["status"] == create_payload["status"]

        # ----------------------------
        # Get Ticket
        # ----------------------------
        get_response = await client.get(f"/tickets/ticket/{ticket_id}")

        assert get_response.status_code == 200

        fetched_ticket = get_response.json()["ticket"]

        assert fetched_ticket["id"] == ticket_id
        assert fetched_ticket["title"] == create_payload["title"]

        # ----------------------------
        # Update Ticket
        # ----------------------------
        update_response = await client.put(
            f"/tickets/ticket/{ticket_id}",
            json=update_payload,
        )

        assert update_response.status_code == 200

        updated_ticket = update_response.json()["ticket"]

        assert updated_ticket["title"] == update_payload["title"]
        assert updated_ticket["priority"] == update_payload["priority"]
        assert updated_ticket["status"] == update_payload["status"]

        # ----------------------------
        # Verify Update
        # ----------------------------
        verify_response = await client.get(f"/tickets/ticket/{ticket_id}")

        assert verify_response.status_code == 200

        verified_ticket = verify_response.json()["ticket"]

        assert verified_ticket["title"] == update_payload["title"]
        assert verified_ticket["priority"] == update_payload["priority"]
        assert verified_ticket["status"] == update_payload["status"]

        # ----------------------------
        # Get All Tickets
        # ----------------------------
        list_response = await client.get("/tickets/ticket")

        assert list_response.status_code == 200

        tickets = list_response.json()["tickets"]

        assert any(ticket["id"] == ticket_id for ticket in tickets)

        # ----------------------------
        # Delete Ticket
        # ----------------------------
        delete_response = await client.delete(f"/tickets/ticket/{ticket_id}")

        assert delete_response.status_code == 200

        # ----------------------------
        # Verify Deletion
        # ----------------------------
        get_deleted = await client.get(f"/tickets/ticket/{ticket_id}")

        assert get_deleted.status_code == 404

        # ----------------------------
        # Delete Again
        # ----------------------------
        delete_again = await client.delete(f"/tickets/ticket/{ticket_id}")

        assert delete_again.status_code == 404