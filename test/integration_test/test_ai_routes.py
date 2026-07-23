import pytest
from httpx import AsyncClient
from app.main import app
from app.api.ai import get_bedrock_service
from app.service.aws.bedrock_service import FakeBedrockService, BedrockServiceError


class MockErrorBedrockService:
    def summarize_ticket(self, ticket_description: str) -> dict[str, str]:
        raise BedrockServiceError("Bedrock request failed")


@pytest.mark.asyncio
class TestAIRoutes:

    async def test_summarize_ticket_success(self, client: AsyncClient):
        # Override the dependency to use FakeBedrockService so we don't call real AWS
        app.dependency_overrides[get_bedrock_service] = lambda: FakeBedrockService()

        payload = {
            "ticket_description": "The system keeps throwing a 500 error when I try to save the user profile. Please help fix it."
        }
        response = await client.post("/ai/summarize", json=payload)

        # Clear override
        app.dependency_overrides.pop(get_bedrock_service, None)

        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "suggested_response" in data
        assert data["summary"] == "Support issue: The system keeps throwing a 500 error when I try to save the user prof"

    async def test_summarize_ticket_invalid_payload(self, client: AsyncClient):
        # ticket_description is too short (min_length=10)
        payload = {
            "ticket_description": "Short"
        }
        response = await client.post("/ai/summarize", json=payload)
        assert response.status_code == 422

    async def test_summarize_ticket_service_error(self, client: AsyncClient):
        # Override dependency to return a service that raises BedrockServiceError
        app.dependency_overrides[get_bedrock_service] = lambda: MockErrorBedrockService()

        payload = {
            "ticket_description": "The system keeps throwing a 500 error when I try to save the user profile. Please help fix it."
        }
        response = await client.post("/ai/summarize", json=payload)

        # Clear override
        app.dependency_overrides.pop(get_bedrock_service, None)

        assert response.status_code == 502
        data = response.json()
        assert data["detail"] == "The AI service is temporarily unavailable"
