from logging import Logger
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

from src.config import Settings
from src.domain.custom_exception import CustomException
from src.external_services.pvauth import PvAuth


class HeaderHandlerMiddleware(BaseHTTPMiddleware):

    settings: Settings
    pvauth_service: PvAuth
    logger: Logger

    def __init__(self, app: FastAPI, settings: Settings, pvauth_service: PvAuth, logger: Logger):
        super().__init__(app)
        self.settings = settings
        self.pvauth_service = pvauth_service
        self.logger = logger

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        path = request.url.path
        method = request.method

        if method != 'OPTIONS':
            is_public_endpoint = False
            public_endpoints = self.settings.FASTAPI_PUBLIC_ENDPOINTS

            self.logger.info(f'PATH: {path}')
            self.logger.info(f'METHOD: {method}')

            if public_endpoints:
                for endpoint in public_endpoints:
                    if endpoint.path in path and endpoint.method == method:
                        is_public_endpoint = True

            if not is_public_endpoint:
                user_agent = request.headers.get('User-Agent', '')
                environment = self.settings.FASTAPI_ENV

                self.logger.debug(f'User-Agent {user_agent}')

                if environment == 'local' or self.settings.FASTAPI_USER_AGENT == user_agent:
                    return await call_next(request)

                pvauth_response = await self.pvauth_service.Authentication.Authenticate(request)

                if not pvauth_response:
                    return CustomException(
                        403, 'Access denied'
                    ).to_response()

        response = await call_next(request)
        return response
