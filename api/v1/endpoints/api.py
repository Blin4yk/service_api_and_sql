from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.domain.repositories import IItemRepository, IExternalClient
from core.service.sync_service import SyncService

from infrastructure.external.external_client import ExternalClient

from infrastructure.database.db import SessionLocal, init_db
from infrastructure.database.models.domain import ItemOut
from infrastructure.repo.item_repository import ItemRepository

router = APIRouter()
init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_item_repo(db: Session = Depends(get_db)) -> IItemRepository:
    return ItemRepository(db)

def get_external_client() -> IExternalClient:
    return ExternalClient(base_url='http://localhost:8000/external')

@router.get('/items', response_model=list[ItemOut])
def list_items(repo: IItemRepository = Depends(get_item_repo)):
    return repo.list_active()


@router.post('/sync')
def sync(
    page: int = 1,
    limit: int = 50,
    since: str | None = None,
    repo: IItemRepository = Depends(get_item_repo),
    client: IExternalClient = Depends(get_external_client)
):
    items = client.get_items(page=page, limit=limit, since=since)
    service = SyncService(repo)
    count = service.sync(items)
    return {'synced': count}
