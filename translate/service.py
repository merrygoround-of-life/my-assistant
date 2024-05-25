from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from translate.schemas import TranslateRequest, TranslateChunkResponse


class TranslateService:
    def __init__(self):
        self._client = ChatOpenAI(model="gpt-3.5-turbo")

    async def translate(self, request: TranslateRequest) -> str:
        async for chunk in self._client.astream(input=[
            SystemMessage(content="You are a helpful translator."),
            HumanMessage(content=f"Please translate from {request.from_lang} to {request.to_lang}:"),
            HumanMessage(content=request.input),
        ]):
            yield f"data: {TranslateChunkResponse(output=chunk.content).model_dump_json()}\n\n"
