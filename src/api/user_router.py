from fastapi import APIRouter, Request
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.seedwork.repo.async_session import get_session

router = APIRouter(prefix="/user")


@router.post("/list", summary="user query")
async def user_list(request: Request, name: str = Query(...), session: AsyncSession = Depends(get_session)):
    return
