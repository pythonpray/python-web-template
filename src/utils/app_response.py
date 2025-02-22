from datetime import datetime
from typing import Any, TypeVar, Generic, Optional

from pydantic import BaseModel, Field
from infra.request_context import req_ctx

T = TypeVar("T")


class AppResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    code: int = 200
    message: str = "success"
    request_id: Optional[str] = Field(default_factory=lambda: req_ctx.request_id_ctx.get())
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class ResponseHandler:
    @staticmethod
    def success(data: Any = None, message: str = "success") -> AppResponse:
        return AppResponse(data=data, message=message)

    @staticmethod
    def error(data: Any = None, message: str = "error", code=500) -> AppResponse:
        return AppResponse(data=data, message=message, code=code)
