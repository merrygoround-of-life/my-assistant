from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from translate.schemas import TranslateRequest
from translate.service import TranslateService

router = APIRouter()
logger = getLogger()

TranslateServiceDep = Annotated[TranslateService, Depends()]


@router.post(path="")
async def translate(translate_request: TranslateRequest, translate_service: TranslateServiceDep):
    return StreamingResponse(content=translate_service.translate(translate_request),
                             media_type="text/event-stream")
