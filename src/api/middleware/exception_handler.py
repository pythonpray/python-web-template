from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
import traceback

from src.infra.logger import app_logger
from src.infra.seedwork.api.api_exception import ApiException
from utils.app_response import ResponseHandler


class GlobalExceptionHandler(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ApiException as exc:
            # 处理已知的业务异常，只记录简单的警告信息
            app_logger.warning(f"Business error: {exc.error_code} - {str(exc)}")
            return JSONResponse(status_code=400, content=ResponseHandler.error(exc.error_code, str(exc)).dict())
        except Exception as exc:
            # 对于系统异常，记录更详细的信息
            error_location = traceback.extract_tb(exc.__traceback__)[-1]
            error_context = {
                "path": request.url.path,
                "method": request.method,
                "file": error_location.filename,
                "line": error_location.lineno,
                "function": error_location.name,
            }
            app_logger.error(
                f"System error at {error_context['file']}:{error_context['line']} " f"in {error_context['function']} - {str(exc)}", extra=error_context
            )
            return JSONResponse(status_code=500, content=ResponseHandler.error("SYSTEM_ERROR", "嗯?我真的佛了,这也能报错?你是干啥吃的?").dict())
