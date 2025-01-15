from contextlib import asynccontextmanager
from logging import Logger

from databases import Database
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from src.config import Settings


class SqlAlchemyDatabase():

    basedb: Database
    # * Ejemplo usando una base de datos adicional
    analyticsdb: Database

    def __init__(self, settings: Settings):
        self.basedb = Database(settings.POSTGRES_DB_BASE_URL)
        # * Ejemplo usando una base de datos adicional
        self.analyticsdb = Database(
            settings.POSTGRES_DB_ANALYTICS_URL)

    async def connect(self):
        for _, database in self.__dict__.items():
            await database.connect()

    async def disconnect(self):
        for _, database in self.__dict__.items():
            await database.disconnect()


class DatabaseHandler():

    settings: Settings
    logger: Logger
    database: SqlAlchemyDatabase
    metadata: MetaData

    def __init__(self, settings, logger, database) -> None:
        self.settings = settings
        self.logger = logger
        self.database = database
        self.metadata = MetaData()

    async def connect_database(self):
        await self.database.connect()

    async def disconnect_database(self):
        await self.database.disconnect()

    async def valid_connection_database(self):
        await self.connect_database()
        await self.disconnect_database()

    def init_database(self) -> None:
        for _, db in self.database.__dict__.items():
            self.metadata.bind = create_engine(db.url._url)
