import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

sys.path.insert(0, str(Path(__file__).parent.parent))
import asyncio

import uvicorn
from fastapi import FastAPI

from src.api import api_router
from src.settings.config import get_settings
from api.middleware import load_middleware

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

    load_middleware(app)
    app.include_router(api_router, tags=["api"], prefix=config.app.get("api_prefix"))

    return app


fastapi_app = create_app()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    uvicorn.run("app:fastapi_app", host=config.app["host"], port=int(config.app["port"]), log_config=None, reload=False)
