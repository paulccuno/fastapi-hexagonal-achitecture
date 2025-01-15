from typing import List, Optional
from pydantic_settings import BaseSettings
from src.config.models.endpoint_model import EndpointModel


class Settings(BaseSettings):
    """
    Aqui se especifican las variables de entorno a agregar
    y utilizar en el proyecto
    """

    FASTAPI_APP: str = "app_api"
    FASTAPI_VERSION: str = "1.0.0"
    FASTAPI_ENV: str = 'development'

    FASTAPI_RUN_PORT: int = 11804
    FASTAPI_RUN_HOST: str = "127.0.0.1"
    FASTAPI_CORS_ORIGIN: str = "*"

    FASTAPI_USER_AGENT: str = 'UNIQUE'
    FASTAPI_PUBLIC_ENDPOINTS: Optional[List[EndpointModel]] = None

    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB_BASE: str = "basedb"
    POSTGRES_DB_ANALITYCS: str
    POSTGRES_DB_BASE_URL: Optional[str] = None
    POSTGRES_DB_ANALYTICS_URL: Optional[str] = None

    PVAUTH_API_URL: str
    PVAUTH_API_URL_AUTHENTICATION_AUTHENTICATE: str
    PVAUTH_API_URL_AWS_S3_PRESIGNED: str

    S3_BUCKET_NAME: str
    S3_BUCKET_FOLDER: str

    class Config:
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        """
        Contructor que inicializa las variables ingresadas
        y otras configuraciones necesarias para el proyecto
        """

        super().__init__(**kwargs)

        if not self.POSTGRES_DB_BASE_URL:
            self.POSTGRES_DB_BASE_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB_BASE}"
        if not self.POSTGRES_DB_ANALYTICS_URL:
            self.POSTGRES_DB_ANALYTICS_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB_ANALITYCS}"
