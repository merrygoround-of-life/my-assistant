from pydantic import BaseModel


class ChatRequest(BaseModel):
    input: str


class ChatChunkResponse(BaseModel):
    output: str
