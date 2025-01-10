from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from src.infra.logger import app_logger


class Auth(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception:
            # 只记录日志，让异常继续传播到全局异常处理器
            app_logger.exception("Error in auth middleware")
            raise
