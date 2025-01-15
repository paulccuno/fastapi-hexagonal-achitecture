from dependency_injector import containers, providers
from src.infraestructure.container import AppContainer
from src.external_services.pvauth.container import PvAuthContainer
from src.external_services.aws.container import AwsContainer


class ExternalServicesContainer(containers.DeclarativeContainer):

    app_container: AppContainer = providers.DependenciesContainer()

    config = providers.Configuration()

    # PvAuth Service
    pvauth_container = providers.Container(
        PvAuthContainer, app_container=app_container)
    pvauth_service = pvauth_container().pvauth_service

    # Aws Service
    aws_container = providers.Container(
        AwsContainer, app_container=app_container)
    aws_service = aws_container().aws_service
