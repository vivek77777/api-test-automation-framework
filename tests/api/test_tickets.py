import json
from pathlib import Path

import pytest
from jsonschema import validate

from tests.data.payloads import (
    valid_tenant_payload,
    valid_ticket_payload,
    invalid_ticket_status_payload,
    resolved_ticket_status_payload,
)


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "ticket_schema.json"


def load_ticket_schema():
    with open(SCHEMA_PATH, encoding="utf-8") as schema_file:
        return json.load(schema_file)


@pytest.fixture
def created_tenant(tenants_client):
    response = tenants_client.create_tenant(valid_tenant_payload)
    assert response.status_code == 201
    return response.json()


@pytest.mark.smoke
def test_create_maintenance_ticket_successfully(tickets_client, created_tenant):
    payload = valid_ticket_payload(created_tenant["id"])

    response = tickets_client.create_ticket(payload)

    assert response.status_code == 201

    body = response.json()
    assert body["id"] is not None
    assert body["tenant_id"] == created_tenant["id"]
    assert body["status"] == "open"


@pytest.mark.regression
def test_get_created_maintenance_ticket_by_id(tickets_client, created_tenant):
    create_response = tickets_client.create_ticket(
        valid_ticket_payload(created_tenant["id"])
    )
    ticket_id = create_response.json()["id"]

    get_response = tickets_client.get_ticket(ticket_id)

    assert get_response.status_code == 200
    assert get_response.json()["id"] == ticket_id


@pytest.mark.regression
def test_created_ticket_matches_schema(tickets_client, created_tenant):
    response = tickets_client.create_ticket(valid_ticket_payload(created_tenant["id"]))

    assert response.status_code == 201

    validate(instance=response.json(), schema=load_ticket_schema())


@pytest.mark.regression
def test_update_ticket_status_successfully(tickets_client, created_tenant):
    create_response = tickets_client.create_ticket(
        valid_ticket_payload(created_tenant["id"])
    )
    ticket_id = create_response.json()["id"]

    update_response = tickets_client.update_ticket_status(
        ticket_id,
        resolved_ticket_status_payload,
    )

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "resolved"


@pytest.mark.negative
def test_create_ticket_for_unknown_tenant_returns_404(tickets_client):
    response = tickets_client.create_ticket(valid_ticket_payload("unknown-tenant-id"))

    assert response.status_code == 404
    assert response.json()["detail"] == "Tenant not found"


@pytest.mark.negative
def test_get_unknown_ticket_returns_404(tickets_client):
    response = tickets_client.get_ticket("unknown-ticket-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Maintenance ticket not found"


@pytest.mark.negative
def test_update_ticket_with_invalid_status_returns_400(
    tickets_client,
    created_tenant,
):
    create_response = tickets_client.create_ticket(
        valid_ticket_payload(created_tenant["id"])
    )
    ticket_id = create_response.json()["id"]

    update_response = tickets_client.update_ticket_status(
        ticket_id,
        invalid_ticket_status_payload,
    )

    assert update_response.status_code == 400
    assert update_response.json()["detail"] == "Invalid ticket status"


@pytest.mark.negative
def test_create_ticket_without_auth_returns_401(tickets_client, created_tenant):
    response = tickets_client.create_ticket(
        valid_ticket_payload(created_tenant["id"]),
        headers={},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"