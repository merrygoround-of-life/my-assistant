from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from .models import User, Subject, Group
from .service import UserService, SubjectService, GroupService, GroupSubjectLinkService

router = APIRouter()
logger = getLogger()

UserServiceDep = Annotated[UserService, Depends()]
SubjectServiceDep = Annotated[SubjectService, Depends()]
GroupServiceDep = Annotated[GroupService, Depends()]
GroupSubjectLinkServiceDep = Annotated[GroupSubjectLinkService, Depends()]


@router.post(path="/group")
async def create_group(group: Group, group_service: GroupServiceDep) -> Group:
    return await group_service.create(group)


@router.get(path="/group/{group_id}")
async def get_group(group_id: int, group_service: GroupServiceDep) -> Group:
    group = await group_service.get_by_id(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return group


@router.delete(path="/group/{group_id}")
async def delete_group(group_id: int, group_service: GroupServiceDep):
    group = await group_service.get_by_id(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    await group_service.delete(group)
    return JSONResponse(content="OK")


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
async def delete_user(user_id: int, user_service: UserServiceDep):
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user_service.delete(user)
    return JSONResponse(content="OK")


@router.post(path="/subject")
async def create_subject(subject: Subject, subject_service: SubjectServiceDep) -> Subject:
    return await subject_service.create(subject)


@router.get(path="/subject")
async def list_subject_by_owner_id(owner_id: int, subject_service: SubjectServiceDep) -> list[Subject]:
    return await subject_service.list_by_owner_id(owner_id)


@router.get(path="/subject/{subject_id}")
async def get_subject(subject_id: int, subject_service: SubjectServiceDep) -> Subject:
    subject = await subject_service.get_by_id(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject


@router.delete(path="/subject/{subject_id}")
async def delete_subject(subject_id: int, subject_service: SubjectServiceDep):
    subject = await subject_service.get_by_id(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    await subject_service.delete(subject)
    return JSONResponse(content="OK")


@router.put(path="/group/{group_id}/subject/{subject_id}")
async def create_link(group_id: int, subject_id: int,
                      group_service: GroupServiceDep, subject_service: SubjectServiceDep,
                      group_subject_link_service: GroupSubjectLinkServiceDep):
    group = await group_service.get_by_id(group_id)
    subject = await subject_service.get_by_id(subject_id)
    if not (group and subject):
        raise HTTPException(status_code=404, detail="Group or subject not found")

    await group_subject_link_service.create(group, subject)
    return JSONResponse(content="OK")


@router.delete(path="/group/{group_id}/subject/{subject_id}")
async def delete_link(group_id: int, subject_id: int,
                      group_service: GroupServiceDep, subject_service: SubjectServiceDep,
                      group_subject_link_service: GroupSubjectLinkServiceDep):
    group = await group_service.get_by_id(group_id)
    subject = await subject_service.get_by_id(subject_id)
    if not (group and subject):
        raise HTTPException(status_code=404, detail="Group or subject not found")

    await group_subject_link_service.delete(group, subject)
    return JSONResponse(content="OK")
