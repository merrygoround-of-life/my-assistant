from typing import Annotated

from fastapi import Depends
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage, BaseMessageChunk
from langchain_core.messages.utils import message_chunk_to_message, convert_to_messages
from langchain_openai import ChatOpenAI

from history.models import History
from history.service import HistoryService
from translate.schemas import TranslateRequest, TranslateChunkResponse

HistoryServiceDep = Annotated[HistoryService, Depends()]


class TranslateService:
    def __init__(self, history_service: HistoryServiceDep):
        self._history_service = history_service
        self._client = ChatOpenAI(model="gpt-3.5-turbo")

    async def translate(self, user_id: int, subject_id: int, request: TranslateRequest) -> str:
        messages: list[BaseMessage] = [SystemMessage(content="You are a helpful translator.")]

        async for history in self._history_service.get_history(user_id=user_id, subject_id=subject_id):
            messages += convert_to_messages([history.message])

        human_messages = [
            HumanMessage(content=f"Please translate from {request.from_lang} to {request.to_lang}:"),
            HumanMessage(content=request.input)
        ]

        for human_message in human_messages:
            messages.append(human_message)
            history = History(user=user_id, subject=subject_id, message=human_message.dict())
            await self._history_service.add_history(history)

        merged: BaseMessageChunk | None = None
        async for chunk in self._client.astream(input=messages):
            response_meta = chunk.response_metadata
            if response_meta and "finish_reason" in response_meta and response_meta["finish_reason"] == "stop":
                if merged:
                    message = message_chunk_to_message(merged)
                    history = History(user=user_id, subject=subject_id, message=message.dict())
                    await self._history_service.add_history(history)
            else:
                merged = merged + chunk if merged else chunk

            yield f"data: {TranslateChunkResponse(output=chunk.content).model_dump_json()}\n\n"
