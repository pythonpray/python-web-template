from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class Auth(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            raise exc
