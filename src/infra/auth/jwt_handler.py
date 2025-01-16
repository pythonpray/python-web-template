from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException

from infra.logger import app_logger
from settings.config import get_settings

jwt_auth = get_settings().jwt

JWT_SECRET = jwt_auth.jwt_secret
JWT_ALGORITHM = jwt_auth.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_auth.access_token_expire_minutes


class JWTHandler:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

        to_encode.update({"exp": expire})
        try:
            encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return encoded_jwt
        except Exception as e:
            app_logger.error(f"Error creating JWT token: {str(e)}")
            raise HTTPException(status_code=500, detail="Could not create access token")

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded_token
        except jwt.ExpiredSignatureError:
            app_logger.warning("Token has expired")
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.PyJWTError as e:
            app_logger.error(f"Error verifying token: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid token")
