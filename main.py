from fastapi import FastAPI

from database import init_db
from entity.router import router as entity_router
from translate.router import router as translate_router

app = FastAPI()

app.include_router(entity_router, prefix="/api/v1/entity", tags=["entity"])
app.include_router(translate_router, prefix="/api/v1/translate", tags=["translation"])


# for development purpose only
@app.post("/initdb")
async def initdb():
    await init_db()
