from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from settings import settings

_DATABASE_URL = "postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"

_meta_url = _DATABASE_URL.format(host=settings.pg_host,
                                 port=settings.pg_port,
                                 username=settings.pg_username,
                                 password=settings.pg_password,
                                 database=settings.pg_database)
_engine = create_async_engine(_meta_url, echo=True)
_async_session_factory = async_sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    import entity.models   # noqa
    async with _engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db_session() -> AsyncSession:
    async with _async_session_factory.begin() as session:
        yield session
