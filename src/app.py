from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncio

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.api import api_router
from src.settings.config import get_settings
from api.middleware import load_middleware
from utils.app_response import ResponseHandler

config = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    # Startup
    yield
    # shutdown


def create_app() -> FastAPI:
    if config.app.get("env") == "prod":
        app = FastAPI(title="绝对直觉", description="project", version="1.0.0", docs_url=None, redoc_url=None)
    else:
        app = FastAPI(title="绝对直觉", description="project", version="1.0.0")

    # 注册验证错误处理器
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        if errors:
            error = errors[0]
            field = " -> ".join(str(loc) for loc in error.get("loc", []))
            msg = f"参数错误: {field} - {error.get('msg', '未知错误')}"
        else:
            msg = "请求参数验证失败"

        return JSONResponse(status_code=422, content=ResponseHandler.error("", msg, 422).dict())

    load_middleware(app)
    app.include_router(api_router, tags=["api"], prefix=config.app.get("api_prefix"))

    return app


fastapi_app = create_app()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    uvicorn.run("app:fastapi_app", host=config.app["host"], port=int(config.app["port"]), log_config=None, reload=False)
