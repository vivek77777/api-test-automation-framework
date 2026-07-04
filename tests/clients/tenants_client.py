from tests.clients.base_client import BaseClient


class TenantsClient(BaseClient):
    def create_tenant(self, payload, headers=None):
        return self.post("/tenants", json=payload, headers=headers)

    def get_tenant(self, tenant_id, headers=None):
        return self.get(f"/tenants/{tenant_id}", headers=headers)