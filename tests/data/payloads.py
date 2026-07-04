valid_tenant_payload = {
    "first_name": "Alex",
    "last_name": "Morgan",
    "email": "alex.morgan@example.com",
    "unit_number": "1204",
}

duplicate_tenant_payload = {
    "first_name": "Alex",
    "last_name": "Morgan",
    "email": "alex.morgan@example.com",
    "unit_number": "1204",
}

invalid_tenant_missing_email_payload = {
    "first_name": "Alex",
    "last_name": "Morgan",
    "unit_number": "1204",
}

invalid_tenant_email_payload = {
    "first_name": "Alex",
    "last_name": "Morgan",
    "email": "not-an-email",
    "unit_number": "1204",
}


def valid_ticket_payload(tenant_id):
    return {
        "tenant_id": tenant_id,
        "issue_type": "plumbing",
        "description": "Kitchen sink is leaking",
        "priority": "high",
    }


invalid_ticket_status_payload = {
    "status": "invalid_status"
}

resolved_ticket_status_payload = {
    "status": "resolved"
}