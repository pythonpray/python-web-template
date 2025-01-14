from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
import traceback
import json
import shlex

from src.infra.logger import app_logger
from src.infra.seedwork.api.api_exception import ApiException
from utils.app_response import ResponseHandler


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


class GlobalExceptionHandler(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # 记录请求信息
            curl_command = await request_to_curl(request)
            app_logger.info(f"Incoming request: {request.method} {request.url.path}")
            app_logger.info(f"Request as curl: {curl_command}")

            response = await call_next(request)
            return response

        except ApiException as exc:
            # 处理已知的业务异常，记录curl信息
            curl_command = await request_to_curl(request)
            app_logger.warning(f"Business error: {exc.error_code} - {str(exc)}\nRequest as curl: {curl_command}")
            return JSONResponse(status_code=400, content=ResponseHandler.error(exc.error_code, str(exc)).dict())
        except Exception as exc:
            # 对于系统异常，记录更详细的信息
            curl_command = await request_to_curl(request)
            error_location = traceback.extract_tb(exc.__traceback__)[-1]
            error_context = {
                "path": request.url.path,
                "method": request.method,
                "file": error_location.filename,
                "line": error_location.lineno,
                "function": error_location.name,
            }
            app_logger.error(
                f"System error at {error_context['file']}:{error_context['line']} "
                f"in {error_context['function']} - {str(exc)}\n"
                f"Request as curl: {curl_command}",
                extra=error_context,
            )
            return JSONResponse(status_code=500, content=ResponseHandler.error("SYSTEM_ERROR", "嗯?我真的佛了,这也能报错?你是干啥吃的?").dict())
