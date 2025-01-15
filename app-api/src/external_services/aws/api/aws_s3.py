import base64
import io
from botocore.exceptions import NoCredentialsError
from logging import Logger

from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from src.config import Settings
from src.external_services.aws.api.aws_session import AwsSession


class AwsS3:

    aws_session: AwsSession
    settings: Settings
    logger: Logger
    client: object
    bucket: str

    def __init__(self, aws_session: AwsSession, settings: Settings, logger: Logger) -> None:
        self.aws_session = aws_session
        self.settings = settings
        self.client = self.aws_session.client('s3')
        self.bucket = self.settings.S3_BUCKET_NAME
        self.logger = logger

    async def upload_file(self, file: UploadFile = File(...)):
        try:
            file = file.name
            self.client.upload_fileobj(
                file.file, self.bucket, file.filename)
            return f'{self.bucket}{file.filename}'
        except NoCredentialsError:
            raise 'Credenciales no válidas'

    def upload_file_base64(self, filename: str, content: str):
        try:
            self.logger.info(
                f"Subiendo archivo en base64: filename: {filename}, content: {content}")
            self.logger.info(f"Bucket: {self.bucket}")
            if (content):
                file_content = base64.b64decode(content)
                self.client.upload_fileobj(io.BytesIO(
                    file_content), self.bucket, filename)
            file_url = f"https://{self.bucket}.s3.{self.client.meta.region_name}.amazonaws.com/{filename}"
            self.logger.info(f"URL del archivo subido: {file_url}")
            return file_url
        except NoCredentialsError:
            self.logger.error("Credenciales no válidas")
            raise 'Credenciales no válidas'
        except Exception as e:
            self.logger.error(f"Error S3: {str(e)}")
            raise str(e)

    async def download_file(self, file_name: str):
        try:
            file_path = f"{file_name}"
            self.client.download_file(self.bucket, file_name, file_path)
            return FileResponse(file_path, filename=file_name)
        except NoCredentialsError:
            raise 'Credenciales no válidas'
        except Exception as e:
            raise str(e)
