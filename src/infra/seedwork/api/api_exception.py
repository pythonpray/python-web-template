from typing import Any

from fastapi import HTTPException
from infra.logger import app_logger


class ApiException(HTTPException):
    error_code: int = 400

    def __init__(self, *args: Any) -> None:
        super().__init__(status_code=self.error_code, detail=str(args[0]) if args else None)
        app_logger.warning(f"{self.__class__.__name__} ({self.error_code}): {self.args[0]}")


class BadRequestException(ApiException):
    error_code = 400


class UnauthorizedException(ApiException):
    error_code = 401

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        app_logger.warning(f"{self.__class__.__name__} ({self.error_code}): {self.args[0]}")


class NotFoundException(ApiException):
    error_code = 404


class ConflictException(ApiException):
    error_code = 409


class InternalServerErrorException(ApiException):
    error_code = 500
