from typing import Annotated

from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from database import get_db_session
from entity.models import User, Subject

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


class UserRepository:
    def __init__(self, session: SessionDep):
        self._session = session

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = (await self._session.exec(statement)).first()
        return result

    async def delete(self, user: User) -> None:
        await self._session.delete(user)
        await self._session.flush()


class SubjectRepository:
    def __init__(self, session: SessionDep):
        self._session = session

    async def create(self, subject: Subject) -> Subject:
        self._session.add(subject)
        await self._session.flush()
        return subject

    async def get_by_id(self, subject_id: int) -> Subject | None:
        statement = select(Subject).where(Subject.id == subject_id)
        result = (await self._session.exec(statement)).first()
        return result

    async def list_by_user_id(self, user_id: int) -> list[Subject]:
        statement = select(Subject).join(User).where(User.id == user_id)
        result = list((await self._session.exec(statement)).all())
        return result

    async def delete(self, subject: Subject) -> None:
        await self._session.delete(subject)
        await self._session.flush()
