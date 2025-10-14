from typing import List

from core.domain.models import ItemIn
from core.domain.repositories import IItemRepository


class SyncService:
    def __init__(self, repo: IItemRepository):
        self.repo = repo

    def sync(self, items: List[ItemIn]) -> int:
        try:
            self.repo.upsert_many(items)
            return len(items)
        except Exception:
            raise
