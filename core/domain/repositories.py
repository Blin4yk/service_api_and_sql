from abc import ABC, abstractmethod
from typing import List

from core.domain.models import ItemIn, ItemOut


class IItemRepository(ABC):
    @abstractmethod
    def upsert_many(self, items: List[ItemIn]) -> None:
        pass

    @abstractmethod
    def list_active(self) -> List[ItemOut]:
        pass


class IExternalClient(ABC):
    @abstractmethod
    def get_items(self, page: int, limit: int, since: str | None) -> List[ItemIn]:
        pass
