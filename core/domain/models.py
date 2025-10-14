from datetime import datetime

from pydantic import BaseModel


class ItemBase(BaseModel):
    id: int
    name: str
    updated_at: datetime


class ItemIn(ItemBase):
    is_deleted: bool = False


class ItemOut(ItemBase):
    pass
