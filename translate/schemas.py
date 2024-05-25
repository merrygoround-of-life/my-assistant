from pydantic import BaseModel


class TranslateRequest(BaseModel):
    input: str
    from_lang: str
    to_lang: str


class TranslateChunkResponse(BaseModel):
    output: str
