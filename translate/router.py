from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from history.service import HistoryService
from translate.schemas import TranslateRequest
from translate.service import TranslateService

router = APIRouter()
logger = getLogger()

TranslateServiceDep = Annotated[TranslateService, Depends()]
HistoryServiceDep = Annotated[HistoryService, Depends()]


@router.post(path="/user/{user_id}/subject/{subject_id}")
async def translate(user_id: int,
                    subject_id: int,
                    translate_request: TranslateRequest,
                    translate_service: TranslateServiceDep):
    return StreamingResponse(content=translate_service.translate(user_id=user_id,
                                                                 subject_id=subject_id,
                                                                 request=translate_request),
                             media_type="text/event-stream")
