from typing import Annotated

from fastapi import Depends

from entity.models import User, Subject
from entity.repository import UserRepository, SubjectRepository

UserRepositoryDep = Annotated[UserRepository, Depends()]
SubjectRepositoryDep = Annotated[SubjectRepository, Depends()]


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

    async def list_by_user_id(self, user_id: int) -> list[Subject]:
        return await self._repository.list_by_user_id(user_id)

    async def delete(self, subject: Subject) -> None:
        return await self._repository.delete(subject)
