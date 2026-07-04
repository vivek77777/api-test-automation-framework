import json
from pathlib import Path

import pytest
from jsonschema import validate

from tests.data.payloads import (
    valid_tenant_payload,
    duplicate_tenant_payload,
    invalid_tenant_missing_email_payload,
    invalid_tenant_email_payload,
)


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "tenant_schema.json"


def load_tenant_schema():
    with open(SCHEMA_PATH, encoding="utf-8") as schema_file:
        return json.load(schema_file)


@pytest.mark.smoke
def test_create_tenant_successfully(tenants_client):
    response = tenants_client.create_tenant(valid_tenant_payload)

    assert response.status_code == 201

    body = response.json()
    assert body["id"] is not None
    assert body["email"] == valid_tenant_payload["email"]
    assert body["status"] == "active"


@pytest.mark.regression
def test_get_created_tenant_by_id(tenants_client):
    create_response = tenants_client.create_tenant(valid_tenant_payload)
    tenant_id = create_response.json()["id"]

    get_response = tenants_client.get_tenant(tenant_id)

    assert get_response.status_code == 200
    assert get_response.json()["id"] == tenant_id


@pytest.mark.regression
def test_created_tenant_matches_schema(tenants_client):
    response = tenants_client.create_tenant(valid_tenant_payload)

    assert response.status_code == 201

    validate(instance=response.json(), schema=load_tenant_schema())


@pytest.mark.negative
def test_create_tenant_without_auth_returns_401(tenants_client):
    response = tenants_client.create_tenant(valid_tenant_payload, headers={})

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


@pytest.mark.negative
def test_create_duplicate_tenant_returns_409(tenants_client):
    first_response = tenants_client.create_tenant(valid_tenant_payload)
    assert first_response.status_code == 201

    duplicate_response = tenants_client.create_tenant(duplicate_tenant_payload)

    assert duplicate_response.status_code == 409
    assert duplicate_response.json()["detail"] == "Tenant email already exists"


@pytest.mark.negative
def test_create_tenant_missing_required_email_returns_422(tenants_client):
    response = tenants_client.create_tenant(invalid_tenant_missing_email_payload)

    assert response.status_code == 422


@pytest.mark.negative
def test_create_tenant_invalid_email_returns_422(tenants_client):
    response = tenants_client.create_tenant(invalid_tenant_email_payload)

    assert response.status_code == 422


@pytest.mark.negative
def test_get_unknown_tenant_returns_404(tenants_client):
    response = tenants_client.get_tenant("unknown-tenant-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tenant not found"