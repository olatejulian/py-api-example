from typing import Any

from beanie import init_beanie
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)

from .config import BaseConfig


class DatabaseConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.name = self._get("DATABASE_NAME")
        self.uri = self._get("DATABASE_URI")


class Database:
    client: AsyncIOMotorClient
    database: AsyncIOMotorDatabase
    session: AsyncIOMotorClientSession

    def __init__(self, config: DatabaseConfig, models: list[Any]) -> None:
        self.client = AsyncIOMotorClient(config.uri)

        self.database = self.client[config.name]

        self.models = models

    async def connect(self) -> None:
        await init_beanie(database=self.database, document_models=self.models)

        self.session = await self.client.start_session()
