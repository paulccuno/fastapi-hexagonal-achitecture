import json
from fastapi import Request
from httpx import AsyncClient
from logging import Logger

from src.config import Settings
from src.domain.custom_exception import CustomException


class PvAuthentication:

    settings: Settings
    http_client: AsyncClient
    logger: Logger

    def __init__(self, settings: Settings, http_client: AsyncClient, logger: Logger) -> None:
        self.settings = settings
        self.http_client = http_client
        self.logger = logger

    def Test(self, txt: str) -> str:
        return txt + '- procesado por PvAuthentication'

    async def Authenticate(self, request: Request) -> bool:
        url = f'{self.settings.PVAUTH_API_URL}{self.settings.PVAUTH_API_URL_AUTHENTICATION_AUTHENTICATE}'

        code = request.headers.get('Code')
        header = request.headers.get('Header')

        self.logger.debug(f'Code: {code}')
        self.logger.debug(f'Header: {header}')

        if not code or not header:
            raise CustomException(
                status=401, message='Code or Header is missing')

        headers = {
            'Content-Type': 'application/json',
            'trexa': request.url.path,
            'trexb': request.method,
        }

        content = {
            'Code': code,
            'Header': header,
        }

        content_serialized = json.dumps(content)

        response = await self.http_client.post(
            url,
            headers=headers,
            content=content_serialized,
        )

        self.logger.debug(
            f'Response GetHeaderValidate: {str(response.__dict__)}')

        if response.is_success:
            return response.json()

        return False
