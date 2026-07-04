class BaseClient:
    def __init__(self, client):
        self.client = client
        self.auth_headers = {"Authorization": "Bearer test-token"}

    def _resolve_headers(self, headers):
        if headers is None:
            return self.auth_headers

        return headers

    def get(self, url, headers=None):
        return self.client.get(url, headers=self._resolve_headers(headers))

    def post(self, url, json=None, headers=None):
        return self.client.post(
            url,
            json=json,
            headers=self._resolve_headers(headers),
        )

    def patch(self, url, json=None, headers=None):
        return self.client.patch(
            url,
            json=json,
            headers=self._resolve_headers(headers),
        )