from boto3 import Session
from src.config import Settings


class AwsSession:

    session: Session
    settings: Settings

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.session = Session(region_name=self.settings.AWS_REGION)

    def client(self, service_name):
        return self.session.client(service_name)

    def resource(self, service_name):
        return self.session.resource(service_name)
