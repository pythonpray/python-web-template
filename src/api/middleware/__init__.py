from .auth import Auth
from .request_context import RequestContextMiddleware
from .exception_handler import GlobalExceptionHandler
from fastapi import FastAPI


def load_middleware(app: FastAPI):
    # 注意：中间件的添加顺序很重要
    app.add_middleware(GlobalExceptionHandler)
    app.add_middleware(Auth)
    app.add_middleware(RequestContextMiddleware)
