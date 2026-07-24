from locust import HttpUser, between, task

from app.models.ticket_model import PriorityEnum, StatusEnum


class TicketApiUser(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def check_health(self) -> None:
        self.client.get("/health", name="GET /health")

    @task(1)
    def list_tickets(self) -> None:
        self.client.get("/tickets/ticket", name="GET /tickets/ticket")

    # @task(1)
    # def create_ticket(self) -> None:
    #     self.client.post(
    #         "/tickets/ticket",
    #         name="POST /tickets/ticket",
    #         json={
    #             "title": "Load test ticket",
    #             "priority": PriorityEnum.HIGH.value,
    #             "status": StatusEnum.OPEN.value,
    #         },
    #     )