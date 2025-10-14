from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.responses import JSONResponse

fake_api = FastAPI()

_FAKE = [
    {
        "id": 1,
        "name": "alpha",
        "updated_at": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        "is_deleted": False,
    },
    {
        "id": 2,
        "name": "beta",
        "updated_at": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        "is_deleted": True,
    },
    {
        "id": 3,
        "name": "gamma",
        "updated_at": (datetime.utcnow()).isoformat(),
        "is_deleted": False,
    },
]


@fake_api.get("/items")
def list_items(page: int = 1, limit: int = 50, since: str | None = None):
    items = _FAKE[:]
    if since:
        try:
            dt = datetime.fromisoformat(since)
            items = [x for x in items if datetime.fromisoformat(x["updated_at"]) >= dt]
        except Exception:
            pass
    start = (page - 1) * limit
    end = start + limit
    return JSONResponse(items[start:end])
