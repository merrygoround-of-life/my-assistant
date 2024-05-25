from fastapi import FastAPI

from translate.router import router as translate_router

app = FastAPI()

app.include_router(translate_router, prefix="/api/v1", tags=["translation"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
