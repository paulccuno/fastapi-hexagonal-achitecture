from datetime import datetime
import logging

from src.config import Settings


def setup_logger(settings: Settings):
    logger = logging.getLogger(__name__)

    # Obtener el entorno de las variables de entorno
    env = settings.FASTAPI_ENV

    if env == 'development':
        logger.setLevel(logging.DEBUG)
    elif env == 'testing':
        logger.setLevel(logging.INFO)
    elif env == 'production':
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.DEBUG)

    # Crear formato personalizado ERROR - 2024-07-11 10:42:33 - Este es un mensaje de error (ERROR).
    formatter = logging.Formatter(
        '%(levelname)s - %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Crear manejador de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger.level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    date_hour_formated = datetime.now().strftime("%Y%m%d")

    # Directorio donde se almacenaran los logs
    log_directory = f"{__package__.replace('.', '/')}/logs/"

    # Crear manejador de archivo
    file_handler = logging.FileHandler(
        f'{log_directory}{settings.FASTAPI_APP}_{settings.FASTAPI_ENV}_{date_hour_formated}.log'
    )
    file_handler.setLevel(logger.level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
