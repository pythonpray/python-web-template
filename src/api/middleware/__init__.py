from .auth import AuthMiddleware
from .exception_handler import GlobalExceptionHandler
from fastapi import FastAPI


def load_middleware(app: FastAPI):
    # 注意：中间件的添加顺序很重要
    # 异常处理器必须是第一个
    app.add_middleware(GlobalExceptionHandler)
    # 统一的认证中间件
    app.add_middleware(AuthMiddleware)
