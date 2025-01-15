from logging import Logger

from src.external_services.pvauth import PvAuth


class AuthService():

    def __init__(self, pvauth_service: PvAuth, logger: Logger):
        self.pvauth_service = pvauth_service
        self.logger = logger

    async def test(self):
        self.logger.info("Servicio Auth Test")

        auth_response = self.pvauth_service.Authentication.Test('test')
        return auth_response
