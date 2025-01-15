from dependency_injector import containers, providers
from fastapi import FastAPI
from httpx import AsyncClient

from src.config import Settings
from src.config.logging import setup_logger
from src.infraestructure.database.sqlalchemy import DatabaseHandler, SqlAlchemyDatabase
from src.infraestructure.utils.demo_utils import DemoUtils
from src.api.middlewares.error_handler_middleware import ErrorHandlerMiddleware


class AppContainer(containers.DeclarativeContainer):

    app = providers.Singleton(FastAPI)

    config = providers.Configuration()

    # Environment variables settings
    settings = providers.Singleton(Settings)

    logger = providers.Singleton(setup_logger, settings=settings)

    headers = {
        'Content-Type': 'application/json',
    }

    http_client = providers.Singleton(AsyncClient, headers=headers)

    database = providers.Singleton(SqlAlchemyDatabase, settings=settings)
    db_handler = providers.Singleton(
        DatabaseHandler, settings=settings, logger=logger, database=database)

    # Utils
    demo_utils = providers.Singleton(
        DemoUtils, settings=settings, logger=logger)

    # Middlewares
    error_handler_middleware = providers.Singleton(
        ErrorHandlerMiddleware, settings=settings, logger=logger)
