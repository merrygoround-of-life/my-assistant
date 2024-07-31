from typing import Any

from pydantic import BaseModel


class ChatRequest(BaseModel):
    params: dict[str, Any] = {}
    input: str
    without_prompt: bool = False


class ChatChunkResponse(BaseModel):
    output: str
