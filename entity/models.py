from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field, Relationship


class BaseEntity(SQLModel, AsyncAttrs):
    create_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)


class User(BaseEntity, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str

    subjects: list["Subject"] = Relationship(back_populates="user")


class Subject(BaseEntity, table=True):
    id: int | None = Field(default=None, primary_key=True)
    topic: str
    user_id: int | None = Field(default=None, foreign_key="user.id", alias="userId")

    user: User | None = Relationship(back_populates="subjects")
