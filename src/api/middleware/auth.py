from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.infra.auth.jwt_handler import JWTHandler
from src.infra.auth.oapi_handler import OApiHandler
from src.infra.logger import app_logger
from src.infra.request_context import request_context
from src.infra.seedwork.api.api_exception import UnauthorizedException

# 不需要验证的路径
EXEMPT_PATHS = ["/auth/login", "/docs"]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            path = request.url.path

            # 检查是否是豁免路径
            if self._is_exempt_path(path):
                return await call_next(request)

            # 根据路径前缀选择认证方式
            if path.startswith("/oapi"):
                return await self._handle_oapi_auth(request, call_next)
            else:
                return await self._handle_api_auth(request, call_next)

        except Exception as e:
            app_logger.error(f"Error in auth middleware: {str(e)}")
            raise

    async def _handle_api_auth(self, request: Request, call_next):
        """处理普通API认证"""
        # 获取并验证token
        token = self._get_token_from_header(request)
        if not token:
            raise UnauthorizedException("No token provided")

        # 验证token
        payload = JWTHandler.verify_token(token)

        async with request_context() as ctx:
            ctx.user_session_ctx.set({"user": payload, "type": "api"})
            response = await call_next(request)
            response.headers["X-Request-Id"] = ctx.request_id_ctx.get()
            return response

    @staticmethod
    async def _handle_oapi_auth(request: Request, call_next):
        """处理OpenAPI认证"""

        if not OApiHandler.verify_api_key(request):
            raise UnauthorizedException("Invalid API key")

        async with request_context() as ctx:
            ctx.user_session_ctx.set({"user: oapi_user"})
            response = await call_next(request)
            response.headers["X-Request-Id"] = ctx.request_id_ctx.get()
            return response

    @staticmethod
    def _is_exempt_path(path: str) -> bool:
        """检查是否是豁免路径"""
        return any(path.endswith(exempt_path) for exempt_path in EXEMPT_PATHS)

    @staticmethod
    def _get_token_from_header(request: Request) -> Optional[str]:
        """从请求头中获取JWT token"""
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            return None

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return None
            return token
        except ValueError:
            return None
