from .auth import Auth
from .request_context import RequestContextMiddleware
from fastapi import FastAPI


def load_middleware(app: FastAPI):
    app.add_middleware(Auth)
    app.add_middleware(RequestContextMiddleware)
