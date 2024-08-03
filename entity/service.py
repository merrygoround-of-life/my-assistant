from typing import Annotated

from fastapi import Depends, HTTPException

from entity.models import User, Subject, Group
from entity.repository import UserRepository, SubjectRepository, GroupRepository

UserRepositoryDep = Annotated[UserRepository, Depends()]
SubjectRepositoryDep = Annotated[SubjectRepository, Depends()]
GroupRepositoryDep = Annotated[GroupRepository, Depends()]


class GroupService:
    def __init__(self, repository: GroupRepositoryDep):
        self._repository = repository

    async def create(self, group: Group) -> Group:
        return await self._repository.create(group)

    async def get_by_id(self, group_id: int) -> Group | None:
        return await self._repository.get_by_id(group_id)

    async def delete(self, group: Group) -> None:
        return await self._repository.delete(group)


class UserService:
    def __init__(self, repository: UserRepositoryDep):
        self._repository = repository

    async def create(self, user: User) -> User:
        return await self._repository.create(user)

    async def get_by_id(self, user_id: int) -> User | None:
        return await self._repository.get_by_id(user_id)

    async def delete(self, user: User) -> None:
        return await self._repository.delete(user)


class SubjectService:
    def __init__(self, repository: SubjectRepositoryDep):
        self._repository = repository

    async def create(self, subject: Subject) -> Subject:
        return await self._repository.create(subject)

    async def get_by_id(self, subject_id: int) -> Subject | None:
        return await self._repository.get_by_id(subject_id)

    async def list_by_owner_id(self, owner_id: int) -> list[Subject]:
        return await self._repository.list_by_owner_id(owner_id)

    async def delete(self, subject: Subject) -> None:
        return await self._repository.delete(subject)


class GroupSubjectLinkService:
    async def create(self, group: Group, subject: Subject):
        if subject in (await group.awaitable_attrs.subjects):
            raise HTTPException(status_code=409, detail="Subject already exists in the group.")
        group.subjects.append(subject)

    async def delete(self, group: Group, subject: Subject):
        if subject not in (await group.awaitable_attrs.subjects):
            raise HTTPException(status_code=404, detail="Subject not exists in the group.")
        (await group.awaitable_attrs.subjects).remove(subject)
