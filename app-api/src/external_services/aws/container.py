from dependency_injector import containers, providers
from src.infraestructure.container import AppContainer
from src.external_services.aws import Aws
from src.external_services.aws.api.aws_session import AwsSession
from src.external_services.aws.api.aws_dynamodb import AwsDynamoDB
from src.external_services.aws.api.aws_s3 import AwsS3


class AwsContainer(containers.DeclarativeContainer):

    app_container: AppContainer = providers.DependenciesContainer()

    config = providers.Configuration()

    aws_session = providers.Singleton(AwsSession, app_container.settings)

    # Aws Endpoints
    aws_dynamodb = providers.Singleton(
        AwsDynamoDB, aws_session=aws_session, settings=app_container.settings, logger=app_container.logger
    )
    aws_s3 = providers.Singleton(
        AwsS3, aws_session, app_container.settings, app_container.logger
    )

    # Aws Service
    aws_service = providers.Singleton(
        Aws, aws_dynamodb, aws_s3
    )
