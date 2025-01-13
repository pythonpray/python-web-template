import os

from fastapi import APIRouter

api_router = APIRouter()

for py in os.listdir("api"):
    if py.endswith(".py") and py != "__init__.py":
        m_name = py[:-3]
        m = __import__("api." + m_name, fromlist=[m_name])
        router_instance = m.router
        api_router.include_router(router_instance)
        api_router.include_router(router_instance, prefix="oapi")
