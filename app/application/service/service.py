from typing import List
from infrastructure.database.models.domain import ItemIn
from core.repo.repository import ItemRepository


class SyncService:
    def __init__(self, repo: ItemRepository):
        self.repo = repo


    def sync(self, items: List[ItemIn]):
        payload = [i.model_dump() for i in items]
        self.repo.upsert_many(payload)