from typing import List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.domain.models import ItemIn, ItemOut
from core.domain.repositories import IItemRepository
from infrastructure.database.sqlalchemy import Item


class ItemRepository(IItemRepository):
    def __init__(self, session: Session):
        self.session = session

    def upsert_many(self, items: List[ItemIn]) -> None:
        if not items:
            return

        try:
            for item in items:
                obj = Item(
                    id=item.id,
                    name=item.name,
                    updated_at=item.updated_at,
                    is_deleted=item.is_deleted,
                )
                self.session.merge(obj)
            self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            raise
        except Exception:
            self.session.rollback()
            raise

    def list_active(self) -> List[ItemOut]:
        try:
            stmt = select(Item).where(Item.is_deleted == False)
            rows = self.session.execute(stmt).scalars()
            return [ItemOut.model_validate(r.__dict__) for r in rows]
        except SQLAlchemyError:
            raise
