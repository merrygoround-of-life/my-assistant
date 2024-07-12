from chat.schemas import ChatRequest, ChatChunkResponse


class TranslateRequest(ChatRequest):
    from_lang: str
    to_lang: str
