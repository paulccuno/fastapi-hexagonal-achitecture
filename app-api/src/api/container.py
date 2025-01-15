from dependency_injector import containers, providers
from src.api.routers import DirectoryRouter
from src.infraestructure.container import AppContainer
from src.api.middlewares.header_handler_middleware import HeaderHandlerMiddleware
from src.external_services.container import ExternalServicesContainer
from src.infraestructure.repositories.demo_repository import DemoRepository
from src.domain.services.demo_service import DemoService
from src.domain.services.auth_service import AuthService

directory_router = DirectoryRouter(
    base_path='src/api/routers', api_prefix='src.api.routers')


class ApiContainer(containers.DeclarativeContainer):

    app_container: AppContainer = providers.DependenciesContainer()
    external_services_container: ExternalServicesContainer = providers.DependenciesContainer()

    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        packages=directory_router.include_packages(),
    )

    # Middlewares
    header_handler_middleware = providers.Singleton(
        HeaderHandlerMiddleware, settings=app_container.settings, pvauth_service=external_services_container.pvauth_service, logger=app_container.logger
    )

    # Repositories
    demo_repository = providers.Singleton(
        DemoRepository, database=app_container.database, logger=app_container.logger)

    # Services
    demo_service = providers.Factory(
        DemoService, demo_repository=demo_repository, logger=app_container.logger)
    auth_service = providers.Factory(
        AuthService, pvauth_service=external_services_container.pvauth_service, logger=app_container.logger
    )
