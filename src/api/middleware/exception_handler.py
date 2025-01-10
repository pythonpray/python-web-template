from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.infra.logger import app_logger
from src.infra.seedwork.api.api_exception import ApiException
from utils.app_response import ResponseHandler


class GlobalExceptionHandler(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ApiException as exc:
            # 处理已知的业务异常
            app_logger.warning(f"Business exception occurred: {exc}")
            return JSONResponse(status_code=400, content=ResponseHandler.error(exc.error_code, str(exc)).dict())
        except Exception:
            # 处理未知的系统异常
            app_logger.exception("Unexpected error occurred")
            return JSONResponse(status_code=500, content=ResponseHandler.error("SYSTEM_ERROR", "An unexpected error occurred").dict())
