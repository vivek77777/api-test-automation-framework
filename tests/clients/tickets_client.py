from tests.clients.base_client import BaseClient


class TicketsClient(BaseClient):
    def create_ticket(self, payload, headers=None):
        return self.post("/maintenance-tickets", json=payload, headers=headers)

    def get_ticket(self, ticket_id, headers=None):
        return self.get(f"/maintenance-tickets/{ticket_id}", headers=headers)

    def update_ticket_status(self, ticket_id, payload, headers=None):
        return self.patch(
            f"/maintenance-tickets/{ticket_id}/status",
            json=payload,
            headers=headers,
        )