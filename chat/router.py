from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from chat.schemas import ChatRequest
from chat.service import ChatService
from history.service import HistoryService

router = APIRouter()
logger = getLogger()

ChatServiceDep = Annotated[ChatService, Depends()]
HistoryServiceDep = Annotated[HistoryService, Depends()]


@router.post(path="/user/{user_id}/subject/{subject_id}")
async def chat(user_id: int,
               subject_id: int,
               chat_request: ChatRequest,
               chat_service: ChatServiceDep):
    return StreamingResponse(content=chat_service.chat(user_id=user_id,
                                                       subject_id=subject_id,
                                                       request=chat_request),
                             media_type="text/event-stream")
