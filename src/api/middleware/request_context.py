from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from src.infra.logger import app_logger
from src.infra.request_context import request_context


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            async with request_context() as ctx:
                response = await call_next(request)
                response.headers["X-Request-Id"] = ctx.request_id_ctx.get()
                return response
        except Exception:
            # 只记录日志，让异常继续传播到全局异常处理器
            app_logger.error("Error in request context middleware")
            raise
