from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from src.infra.logger import app_logger


class Auth(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception:
            app_logger.error("Error in auth middleware")
            raise
