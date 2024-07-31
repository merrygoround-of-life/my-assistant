from os import environ
from typing import Annotated, Any

from fastapi import Depends, HTTPException
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage, BaseMessageChunk
from langchain_core.messages.utils import message_chunk_to_message, convert_to_messages
from langchain_openai import ChatOpenAI

from entity.models import Subject
from entity.service import SubjectService, UserService
from history.models import History
from history.service import HistoryService
from chat.schemas import ChatRequest, ChatChunkResponse

UserServiceDep = Annotated[UserService, Depends()]
SubjectServiceDep = Annotated[SubjectService, Depends()]
HistoryServiceDep = Annotated[HistoryService, Depends()]


class ChatService:
    _OPENAI_MODEL_CHAT = "gpt-4o-mini"

    def __init__(self,
                 user_service: UserServiceDep,
                 subject_service: SubjectServiceDep,
                 history_service: HistoryServiceDep):
        self._user_service = user_service
        self._subject_service = subject_service
        self._history_service = history_service
        self._client = ChatOpenAI(model=self._OPENAI_MODEL_CHAT)

    async def _generate_messages(self, user_id: int, subject: Subject, request: ChatRequest) -> list[BaseMessage]:
        messages: list[BaseMessage] = [SystemMessage(content=f"You are {subject.system_role}.")]

        async for history in self._history_service.get_history(user_id=user_id, subject_id=subject.id):
            messages += convert_to_messages([history.message])

        human_messages = self.get_prompt_messages(subject, request.params) if not request.without_prompt else []
        human_messages.append(HumanMessage(content=request.input))

        for human_message in human_messages:
            messages.append(human_message)
            history = History(user=user_id, subject=subject.id, message=human_message.dict())
            await self._history_service.add_history(history)

        return messages

    async def chat(self, user_id: int, subject_id: int, request: ChatRequest):
        user = await self._user_service.get_by_id(user_id)
        subject = await self._subject_service.get_by_id(subject_id)
        if not user or not subject:
            raise HTTPException(status_code=400, detail="user or subject not found.")

        messages = await self._generate_messages(user_id, subject, request)

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

            if "IGNORE_SSE_FORMAT" in environ and bool(environ["IGNORE_SSE_FORMAT"]):
                output = f"{chunk.content}"
            else:
                output = f"data: {ChatChunkResponse(output=chunk.content).model_dump_json()}\n\n"
            yield output

    @staticmethod
    def get_prompt_messages(subject: Subject, template_params: dict[str, Any]) -> list[HumanMessage]:
        template = subject.prompt_template

        for key, value in template_params.items():
            template = template.replace(f"{{{key}}}", value)

        messages = [HumanMessage(content=template)] if template else []

        return messages
