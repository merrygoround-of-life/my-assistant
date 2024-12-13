import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from slack_bolt.adapter.socket_mode.websockets import AsyncSocketModeHandler

from .database import init_db
from .entity.router import router as entity_router
from .history.service import HistoryService
from .chat.router import router as chat_router
from .slack.listener import slack_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        singleton_history_service = HistoryService()
        app.dependency_overrides[HistoryService] = lambda: singleton_history_service

        socket_handler = AsyncSocketModeHandler(slack_app, os.environ.get("SLACK_APP_TOKEN"))
        await socket_handler.connect_async()
        yield
    finally:
        app.dependency_overrides = {}


app = FastAPI(lifespan=lifespan)

app.include_router(entity_router, prefix="/api/v1/entity", tags=["entity"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])


# for development purpose only
@app.post("/initdb")
async def initdb():
    await init_db()
    return JSONResponse(content="OK")
