from .auth import AuthMiddleware
from .exception_handler import GlobalExceptionHandler
from fastapi import FastAPI


def load_middleware(app: FastAPI):
    app.add_middleware(GlobalExceptionHandler)
    app.add_middleware(AuthMiddleware)
