from typing import Any

from pydantic import BaseModel


class ChatRequest(BaseModel):
    params: dict[str, Any] = {}
    input: str


class ChatChunkResponse(BaseModel):
    output: str
