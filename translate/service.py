from typing import Annotated

from fastapi import Depends
from langchain_core.messages import SystemMessage, HumanMessage

from chat.schemas import ChatRequest
from chat.service import ChatService
from history.service import HistoryService
from translate.schemas import TranslateRequest

HistoryServiceDep = Annotated[HistoryService, Depends()]


class TranslateService(ChatService):
    def __init__(self, history_service: HistoryServiceDep):
        super().__init__(history_service)

    def get_system_message(self) -> SystemMessage:
        return SystemMessage(content="You are a helpful translator.")

    def get_human_messages(self, request: ChatRequest) -> list[HumanMessage]:
        assert isinstance(request, TranslateRequest)
        return [
            HumanMessage(content=f"Please translate from {request.from_lang} to {request.to_lang}:"),
            HumanMessage(content=request.input)
        ]
