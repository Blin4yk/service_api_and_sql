from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from infrastructure.database.sqlalchemy import Item
from core.domain.repositories import IItemRepository
from core.domain.models import ItemIn, ItemOut

class ItemRepository(IItemRepository):
    def __init__(self, session: Session):
        self.session = session

    def upsert_many(self, items: List[ItemIn]) -> None:
        for item in items:
            obj = self.session.get(Item, item.id) or Item(id=item.id)
            obj.name = item.name
            obj.updated_at = item.updated_at
            obj.is_deleted = item.is_deleted
            self.session.add(obj)
        self.session.commit()

    def list_active(self) -> List[ItemOut]:
        stmt = select(Item).where(Item.is_deleted == False)
        rows = self.session.execute(stmt).scalars()
        return [ItemOut.model_validate(r.__dict__) for r in rows]