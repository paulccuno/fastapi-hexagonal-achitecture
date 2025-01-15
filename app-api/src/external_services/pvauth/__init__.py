from src.external_services.pvauth.api.pvauth_authentication import PvAuthentication
from src.external_services.pvauth.api.pvauth_aws import PvAuthAws


class PvAuth:

    Authentication: PvAuthentication
    Aws: PvAuthAws

    def __init__(self, Authentication: PvAuthentication, Aws: PvAuthAws) -> None:
        self.Authentication = Authentication
        self.Aws = Aws
