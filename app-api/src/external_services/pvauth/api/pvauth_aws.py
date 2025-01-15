import json
from logging import Logger
from typing import Union
from httpx import AsyncClient
from src.config import Settings
from src.external_services.pvauth.models.s3_presigned_request import S3PresignedRequest
from src.external_services.pvauth.models.s3_presigned_response import S3PresignedResponse


class PvAuthAws:

    settings: Settings
    http_client: AsyncClient
    logger: Logger

    def __init__(self, settings: Settings, http_client: AsyncClient, logger: Logger) -> None:
        self.settings = settings
        self.http_client = http_client
        self.logger = logger

    async def S3Presigned(self, code: str, header: str, entity: S3PresignedRequest) -> Union[S3PresignedResponse, None]:
        url = f'{self.settings.PVAUTH_API_URL}{self.settings.PVAUTH_API_URL_AWS_S3_PRESIGNED}'
        self.logger.debug(f'URL: {url}')

        headers = {
            'Content-Type': 'application/json',
            'Code': code,
            'Header': header,
        }

        content = json.dumps(entity.dict())
        self.logger.debug(f'Content: {str(content)}')

        response = await self.http_client.request(
            'GET',
            url,
            headers=headers,
            content=content
        )

        if response.is_success:
            response_adapted = S3PresignedResponse(**response.json())
            self.logger.debug(f'Response: {str(response_adapted)}')
            return response_adapted

        return None
