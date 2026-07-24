from __future__ import annotations

import json
import os
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.schemas.ticket_schema import TicketInSchema
from app.service.aws.prompt_template import PromptLoader
from dotenv import load_dotenv

load_dotenv()


class BedrockServiceError(RuntimeError):
    pass


class BedrockService:
    """Wrapper around the Amazon Bedrock Converse API.

    The boto3 client is injectable, allowing deterministic unit tests without
    live network calls or model cost.
    """

    def __init__(
            self,
            client: Any | None = None,
    ) -> None:
        self.model_id = os.getenv("BEDROCK_MODEL_ID")
        self.client = client or boto3.client(
            "bedrock-runtime",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )
        self.prompt_loader = PromptLoader()

    def summarize_ticket(self, ticket_description: str, ticket_list: str = "") -> dict[str, str]:
        prompt = self.prompt_loader.render(
            "ticket_summary",
            ticket_description=ticket_description,
            ticket_list=ticket_list,
        )
        try:
            response = self.client.converse(
                modelId=self.model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}],
                    }
                ],
                inferenceConfig={
                    "maxTokens": 350,
                    "temperature": 0.1,
                },
            )
        except (BotoCoreError, ClientError) as exc:
            print(f"AWS Bedrock client error during converse call: {exc}")
            raise BedrockServiceError("Bedrock request failed") from exc

        try:
            print("--- Bedrock Raw Response Output ---")
            text = response["output"]["message"]["content"][0]["text"]
            print(text)
            print("-----------------------------------")
            text = text.strip()
            
            if text.startswith("```"):
                text = "\n".join(line for line in text.splitlines()[1:] if not line.strip().startswith("```"))
                text = text.strip()
            
            parsed = None
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                # Attempt to extract JSON using { } boundaries
                start_idx = text.find("{")
                end_idx = text.rfind("}")
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    try:
                        parsed = json.loads(text[start_idx:end_idx+1])
                    except json.JSONDecodeError:
                        pass
            
            # If still not parsed, treat the entire output as the response
            if not parsed or not isinstance(parsed, dict):
                parsed = {
                    "summary": "AI Desk Response",
                    "suggested_response": text
                }

            return {
                "summary": str(parsed.get("summary", "AI Desk Response")),
                "suggested_response": str(parsed.get("suggested_response", text)),
            }
        except Exception as exc:
            print(f"Error parsing Bedrock response: {exc}")
            raise BedrockServiceError("Bedrock returned an invalid response") from exc
    def generate_description(self, ticket_input: TicketInSchema) -> str:
        prompt = self.prompt_loader.render(
            "generate_description",
            title=ticket_input.title,
            priority=ticket_input.priority,
            status=ticket_input.status,
        )

        try:
            response = self.client.converse(
                modelId=self.model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}],
                    }
                ],
                inferenceConfig={
                    "maxTokens": 100,
                    "temperature": 0.1,
                },
            )
        except (BotoCoreError, ClientError) as exc:
            raise BedrockServiceError("Bedrock request failed") from exc

        try:
            return response["output"]["message"]["content"][0]["text"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise BedrockServiceError("Invalid Bedrock response") from exc

class FakeBedrockService:
    """Offline deterministic implementation for classroom demonstrations."""

    def summarize_ticket(self, ticket_description: str, ticket_list: str = "") -> dict[str, str]:
        short_description = ticket_description.strip()[:70]
        return {
            "summary": f"Support issue: {short_description}",
            "suggested_response": (
                "Acknowledge the issue, confirm that it is being investigated, "
                "and provide the next expected update."
            ),
        }
