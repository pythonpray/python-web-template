from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import json
import shlex

from src.infra.logger import app_logger


async def request_to_curl(request: Request) -> str:
    """将请求转换为curl命令格式"""
    # 基础URL
    curl_parts = ["curl", "-X", request.method, str(request.url)]

    # 添加请求头
    headers = dict(request.headers)
    for key, value in headers.items():
        if key.lower() not in ["host", "content-length"]:  # 排除一些不需要的头部
            curl_parts.extend(["-H", f"{key}: {value}"])

    # 添加请求体
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
        if body:
            try:
                # 尝试解析为JSON
                body_str = body.decode()
                json.loads(body_str)  # 验证是否为有效的JSON
                curl_parts.extend(["-d", body_str])
            except json.JSONDecoder:
                # 如果不是JSON，则作为普通数据处理
                curl_parts.extend(["--data-raw", body.decode()])

    # 使用shlex.quote确保所有参数都被正确转义
    return " ".join(shlex.quote(str(part)) for part in curl_parts)


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 记录请求信息
        curl_command = await request_to_curl(request)
        app_logger.info(f"Incoming request: {request.method} {request.url.path}")
        app_logger.info(f"Request as curl: {curl_command}")

        response = await call_next(request)
        return response
