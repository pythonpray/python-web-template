from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import AuthMiddleware
from .exception_handler import GlobalExceptionHandlerMiddleware
from .acess_log import AccessLogMiddleware


def load_middleware(app: FastAPI):
    """加载所有中间件"""

    # CORS中间件配置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有源，生产环境应该设置具体的域名
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有HTTP方法
        allow_headers=["*"],  # 允许所有请求头
    )

    app.add_middleware(GlobalExceptionHandlerMiddleware)
    app.add_middleware(AuthMiddleware)
    app.add_middleware(AccessLogMiddleware)
