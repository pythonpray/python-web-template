from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
import traceback

from infra.logger import app_logger
from infra.seedwork.api.api_exception import ApiException
from utils.app_response import ResponseHandler


class GlobalExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except ApiException as exc:
            # 处理已知的业务异常
            app_logger.warning("Business error: %s - %s", exc.error_code, str(exc))
            return JSONResponse(status_code=400, content=ResponseHandler.error(exc.error_code, str(exc)).dict())
        except Exception as exc:
            # 对于系统异常，记录更详细的信息
            error_location = traceback.extract_tb(exc.__traceback__)[-1]
            app_logger.error(
                f"System error at {error_location.filename}:{error_location.lineno} in {error_location.name} - {str(exc)}",
                extra={
                    "path": request.url.path,
                    "method": request.method,
                    "file": error_location.filename,
                    "line": error_location.lineno,
                    "function": error_location.name,
                },
            )
            return JSONResponse(status_code=500, content=ResponseHandler.error("SYSTEM_ERROR", "系统错误，请稍后重试").dict())
