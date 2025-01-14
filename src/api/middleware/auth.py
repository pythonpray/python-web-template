from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.infra.auth.jwt_handler import JWTHandler
from src.infra.auth.oapi_handler import OApiHandler
from src.infra.logger import app_logger
from src.infra.request_context import request_context
from src.infra.seedwork.api.api_exception import UnauthorizedException

# 不需要验证的路径
EXEMPT_PATHS = ["/api/auth/login", "/docs", "/openapi.json", "/", "/static", "/favicon.ico"]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            path = request.url.path

            # 所有请求都在request_context中处理
            async with request_context() as ctx:
                # 检查是否是豁免路径
                if self._is_exempt_path(path):
                    response = await call_next(request)
                    response.headers["X-Request-Id"] = ctx.request_id_ctx.get()
                    return response

                # 根据路径前缀选择认证方式
                if path.startswith("/oapi"):
                    # 验证OpenAPI密钥
                    if not OApiHandler.verify_api_key(request):
                        raise UnauthorizedException("Invalid API key")
                    ctx.user_session_ctx.set({"user": "oapi_user", "type": "oapi"})
                else:
                    # 验证JWT Token
                    token = self._get_token_from_header(request)
                    if not token:
                        raise UnauthorizedException("No token provided")
                    payload = JWTHandler.verify_token(token)
                    ctx.user_session_ctx.set({"user": payload, "type": "api"})

                # 继续处理请求
                response = await call_next(request)
                response.headers["X-Request-Id"] = ctx.request_id_ctx.get()
                return response

        except Exception as e:
            app_logger.error(f"Error in auth middleware: {str(e)}")
            raise

    @staticmethod
    def _is_exempt_path(path: str) -> bool:
        """检查路径是否豁免认证"""
        # 检查完全匹配的路径
        if path in EXEMPT_PATHS:
            return True

        # 检查以豁免路径开头的路径（用于目录）
        for exempt_path in EXEMPT_PATHS:
            if path.startswith(exempt_path + "/"):
                return True

        return False

    @staticmethod
    def _get_token_from_header(request: Request) -> Optional[str]:
        """从请求头中获取token"""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        return parts[1]
