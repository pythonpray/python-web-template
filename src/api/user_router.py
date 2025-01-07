import json
import logging
from typing import List
from typing import Optional, Union

from fastapi import APIRouter, Request, Path, HTTPException
from fastapi.params import Query, Depends, Body, Header

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/user')


@router.post("/list", summary='user query')
async def user_list(request: Request, name: str  = Query(...), session: AsyncSession = Depends(get_session)):

    return