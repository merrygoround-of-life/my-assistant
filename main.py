from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db
from entity.router import router as entity_router
from history.service import HistoryService
from translate.router import router as translate_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        singleton_history_service = HistoryService()
        app.dependency_overrides[HistoryService] = lambda: singleton_history_service
        yield
    finally:
        app.dependency_overrides = {}


app = FastAPI(lifespan=lifespan)

app.include_router(entity_router, prefix="/api/v1/entity", tags=["entity"])
app.include_router(translate_router, prefix="/api/v1/translate", tags=["translation"])


# for development purpose only
@app.post("/initdb")
async def initdb():
    await init_db()
