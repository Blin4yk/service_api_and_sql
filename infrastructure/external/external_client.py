import httpx
from typing import List
from core.domain.repositories import IExternalClient
from core.domain.models import ItemIn


class ExternalClient(IExternalClient):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_items(self, page: int = 1, limit: int = 50, since: str | None = None) -> List[ItemIn]:
        params = {"page": page, "limit": limit}
        if since:
            params["since"] = since

        with httpx.Client(base_url=self.base_url, timeout=5) as client:
            resp = client.get("/items", params=params)
            resp.raise_for_status()
            return [ItemIn(**x) for x in resp.json()]