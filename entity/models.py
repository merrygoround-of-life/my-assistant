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

    proposals: list["Subject"] = Relationship(back_populates="owner")


class Subject(BaseEntity, table=True):
    id: int | None = Field(default=None, primary_key=True)
    topic: str
    system_role: str = Field(default="a helpful assistant", alias="systemRole")
    prompt_template: str = Field(default="", alias="promptTemplate")
    owner_id: int | None = Field(default=None, foreign_key="user.id", alias="ownerId")

    owner: User | None = Relationship(back_populates="proposals")
