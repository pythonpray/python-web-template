from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from infra.auth.jwt_handler import JWTHandler
from infra.logger import app_logger
from infra.seedwork.api.api_exception import UnauthorizedException
from infra.seedwork.repo.async_session import get_session
from utils.app_response import AppResponse, ResponseHandler

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=AppResponse[TokenResponse])
async def login(request: LoginRequest, session: AsyncSession = Depends(get_session)):
    """
    用户登录接口
    """
    try:
        # 这里只是示例，实际应该查询数据库验证用户
        if request.username != "admin" or request.password != "password":
            raise UnauthorizedException("Invalid username or password")

        # 创建访问令牌
        access_token = JWTHandler.create_access_token(data={"sub": request.username})

        app_logger.info(f"User {request.username} logged in successfully")
        return ResponseHandler.success({"access_token": access_token, "token_type": "bearer"})
    except Exception as e:
        app_logger.error(f"Login failed for user {request.username}: {str(e)}")
        raise
