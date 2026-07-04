from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import uuid4

app = FastAPI(title="API Test Automation Demo")

AUTH_TOKEN = "Bearer test-token"

TENANTS = {}
MAINTENANCE_TICKETS = {}


class TenantCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    unit_number: str


class Tenant(TenantCreate):
    id: str
    status: str = "active"


class MaintenanceTicketCreate(BaseModel):
    tenant_id: str
    issue_type: str
    description: str
    priority: str


class MaintenanceTicket(MaintenanceTicketCreate):
    id: str
    status: str = "open"


class TicketStatusUpdate(BaseModel):
    status: str


def require_auth(authorization: Optional[str]) -> None:
    if authorization != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/tenants", status_code=201)
def create_tenant(
    payload: TenantCreate,
    authorization: Optional[str] = Header(None),
):
    require_auth(authorization)

    for tenant in TENANTS.values():
        if tenant["email"] == payload.email:
            raise HTTPException(status_code=409, detail="Tenant email already exists")

    tenant_id = str(uuid4())
    tenant = Tenant(id=tenant_id, **payload.model_dump())
    TENANTS[tenant_id] = tenant.model_dump()

    return TENANTS[tenant_id]


@app.get("/tenants/{tenant_id}")
def get_tenant(
    tenant_id: str,
    authorization: Optional[str] = Header(None),
):
    require_auth(authorization)

    if tenant_id not in TENANTS:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return TENANTS[tenant_id]


@app.post("/maintenance-tickets", status_code=201)
def create_maintenance_ticket(
    payload: MaintenanceTicketCreate,
    authorization: Optional[str] = Header(None),
):
    require_auth(authorization)

    if payload.tenant_id not in TENANTS:
        raise HTTPException(status_code=404, detail="Tenant not found")

    ticket_id = str(uuid4())
    ticket = MaintenanceTicket(id=ticket_id, **payload.model_dump())
    MAINTENANCE_TICKETS[ticket_id] = ticket.model_dump()

    return MAINTENANCE_TICKETS[ticket_id]


@app.get("/maintenance-tickets/{ticket_id}")
def get_maintenance_ticket(
    ticket_id: str,
    authorization: Optional[str] = Header(None),
):
    require_auth(authorization)

    if ticket_id not in MAINTENANCE_TICKETS:
        raise HTTPException(status_code=404, detail="Maintenance ticket not found")

    return MAINTENANCE_TICKETS[ticket_id]


@app.patch("/maintenance-tickets/{ticket_id}/status")
def update_maintenance_ticket_status(
    ticket_id: str,
    payload: TicketStatusUpdate,
    authorization: Optional[str] = Header(None),
):
    require_auth(authorization)

    if ticket_id not in MAINTENANCE_TICKETS:
        raise HTTPException(status_code=404, detail="Maintenance ticket not found")

    allowed_statuses = {"open", "in_progress", "resolved", "closed"}

    if payload.status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Invalid ticket status")

    MAINTENANCE_TICKETS[ticket_id]["status"] = payload.status

    return MAINTENANCE_TICKETS[ticket_id]