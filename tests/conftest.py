import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app, TENANTS, MAINTENANCE_TICKETS
from tests.clients.tenants_client import TenantsClient
from tests.clients.tickets_client import TicketsClient


@pytest.fixture(autouse=True)
def clear_test_data():
    TENANTS.clear()
    MAINTENANCE_TICKETS.clear()


@pytest.fixture
def api_client():
    return TestClient(app)


@pytest.fixture
def tenants_client(api_client):
    return TenantsClient(api_client)


@pytest.fixture
def tickets_client(api_client):
    return TicketsClient(api_client)