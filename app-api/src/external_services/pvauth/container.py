from dependency_injector import containers, providers
from src.infraestructure.container import AppContainer
from src.external_services.pvauth.api.pvauth_authentication import PvAuthentication
from src.external_services.pvauth.api.pvauth_aws import PvAuthAws
from src.external_services.pvauth import PvAuth


class PvAuthContainer(containers.DeclarativeContainer):

    app_container: AppContainer = providers.DependenciesContainer()

    config = providers.Configuration()

    # PvAuth Endpoints
    pvauth_authentication = providers.Singleton(
        PvAuthentication, app_container.settings, app_container.http_client, app_container.logger
    )
    pvauth_aws = providers.Singleton(
        PvAuthAws, app_container.settings, app_container.http_client, app_container.logger
    )

    # PvAuth Service
    pvauth_service = providers.Singleton(
        PvAuth, pvauth_authentication, pvauth_aws
    )
