from beanie import init_beanie
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)

from src.account import BeanieAccountModel
from src.shared import Config


class BeanieMongoDatabaseConfig(Config):
    def __init__(self):
        super().__init__()

        self.name = self._get("DATABASE_NAME")
        self.uri = self._get("DATABASE_URI")


class BeanieMongoDatabase:
    client: AsyncIOMotorClient
    database: AsyncIOMotorDatabase
    session: AsyncIOMotorClientSession

    def __init__(self, config: BeanieMongoDatabaseConfig) -> None:
        self.client = AsyncIOMotorClient(config.uri)

        self.database = self.client[config.name]

    async def connect(self) -> None:
        await init_beanie(
            database=self.database,
            document_models=[BeanieAccountModel],  # type: ignore
        )

        self.session = await self.client.start_session()


async def init_database(config: BeanieMongoDatabaseConfig) -> BeanieMongoDatabase:
    database = BeanieMongoDatabase(config)

    await database.connect()

    return database
