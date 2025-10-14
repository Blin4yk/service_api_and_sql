from fastapi import FastAPI
from api.v1.endpoints.api import router
from infrastructure.external.external import fake_api


app = FastAPI()
app.mount("/external", fake_api)
app.include_router(router)