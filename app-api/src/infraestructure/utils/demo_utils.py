from logging import Logger
from src.config import Settings


class DemoUtils():

    settings: Settings
    logger: Logger

    def __init__(self, settings: Settings, logger: Logger) -> None:
        self.settings = settings
        self.logger = logger

    def example_util(self):
        self.logger.debug('Example Util')
