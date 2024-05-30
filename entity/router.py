from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from entity.models import User, Subject
from entity.service import UserService, SubjectService

router = APIRouter()
logger = getLogger()

UserServiceDep = Annotated[UserService, Depends()]
SubjectServiceDep = Annotated[SubjectService, Depends()]


@router.post(path="/user")
async def create_user(user: User, user_service: UserServiceDep) -> User:
    return await user_service.create(user)


@router.get(path="/user/{user_id}")
async def get_user(user_id: int, user_service: UserServiceDep) -> User:
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete(path="/user/{user_id}")
async def delete_user(user_id: int, user_service: UserServiceDep) -> None:
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user_service.delete(user)


@router.post(path="/subject")
async def create_subject(subject: Subject, subject_service: SubjectServiceDep) -> Subject:
    return await subject_service.create(subject)


@router.get(path="/subject")
async def list_subject_by_user_id(user_id: int, subject_service: SubjectServiceDep) -> list[Subject]:
    return await subject_service.list_by_user_id(user_id)


@router.get(path="/subject/{subject_id}")
async def get_subject(subject_id: int, subject_service: SubjectServiceDep) -> Subject:
    subject = await subject_service.get_by_id(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject


@router.delete(path="/subject/{subject_id}")
async def delete_subject(subject_id: int, subject_service: SubjectServiceDep) -> None:
    subject = await subject_service.get_by_id(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    await subject_service.delete(subject)
