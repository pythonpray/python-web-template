from .auth import AuthMiddleware
from .exception_handler import GlobalExceptionHandlerMiddleware
from .acess_log import AccessLogMiddleware
from fastapi import FastAPI


def load_middleware(app: FastAPI):
    # 中间件的执行顺序是从下到上的，所以我们需要按照相反的顺序添加
    app.add_middleware(GlobalExceptionHandlerMiddleware)
    app.add_middleware(AuthMiddleware)
    app.add_middleware(AccessLogMiddleware)
