from typing import Any

from fastapi.responses import JSONResponse


class CustomException(Exception):
    def __init__(self, status: int, message: str, detail: tuple[Any, ...] = ()) -> None:
        self.status = status
        self.message = message
        self.detail = detail

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status,
            content={
                'status': self.status,
                'message': self.message,
                'detail': self.detail,
            }
        )
