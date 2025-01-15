from logging import Logger
import sys
import traceback
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

from src.config import Settings
from src.domain.custom_exception import CustomException


class ErrorHandlerMiddleware(BaseHTTPMiddleware):

    settings: Settings
    logger: Logger

    def __init__(self, app: FastAPI, settings: Settings, logger: Logger):
        super().__init__(app)
        self.settings = settings
        self.logger = logger

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            response = await call_next(request)
            return response
        except CustomException as exc:
            self.logger.error(f"CustomException: {exc}")

            return exc.to_response()
        except HTTPException as exc:
            self.logger.error(f"HTTPException: {exc.detail}")

            return CustomException(
                exc.status_code, exc.detail, exc.args
            ).to_response()
        except Exception as exc:
            self.logger.error(f"Unhandled Exception: {exc}")

            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_str = "".join(
                traceback.format_exception(exc_type, exc_value, exc_traceback)
            )

            self.logger.error(traceback_str)

            return CustomException(
                500, "Internal Server Error", exc.args
            ).to_response()
