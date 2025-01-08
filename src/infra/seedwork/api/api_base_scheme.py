from pydantic import BaseModel


class BaseScheme(BaseModel):
    pass


class RequestScheme(BaseScheme):
    pass


class RespScheme(BaseScheme):
    class Config:
        from_attributes = True
