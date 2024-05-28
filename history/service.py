from motor.motor_asyncio import AsyncIOMotorClient

from history.models import History
from settings import settings


class HistoryService:
    def __init__(self):
        uri = "mongodb://{username}:{password}@{host}:{port}".format(username=settings.mg_username,
                                                                     password=settings.mg_password,
                                                                     host=settings.mg_host,
                                                                     port=settings.mg_port)

        client = AsyncIOMotorClient(uri)
        self._db = client.get_database(name=f"{settings.mg_database}")

    async def add_history(self, history: History) -> None:
        collection = self._db.history
        result = await collection.insert_one(history.model_dump())
        return result.inserted_id

    async def get_history(self, user_id: int, subject_id: int):
        collection = self._db.history
        async for document in collection.find({"user": user_id, "subject": subject_id}):
            yield History.model_validate(document)
