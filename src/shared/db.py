from typing import Any

from beanie import init_beanie
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)


class Database:
    client: AsyncIOMotorClient
    database: AsyncIOMotorDatabase
    session: AsyncIOMotorClientSession

    def __init__(self, uri: str, db_name: str, models: list[Any]) -> None:
        self.client = AsyncIOMotorClient(uri)

        self.database = self.client[db_name]

        self.models = models

    async def connect(self) -> None:
        await init_beanie(database=self.database, document_models=self.models)

        self.session = await self.client.start_session()
