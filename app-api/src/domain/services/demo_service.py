from logging import Logger
from src.domain.repositories.demo_repository_interface import DemoRepositoryInterface


class DemoService():

    def __init__(self, demo_repository: DemoRepositoryInterface, logger: Logger):
        self.demo_repository = demo_repository
        self.logger = logger

    async def list_demo(self):
        self.logger.info("Servicio de listado de Demo")
        demos = await self.demo_repository.list_demo()
        return demos
