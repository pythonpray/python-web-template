import datetime
import enum
from json import JSONEncoder
from typing import Optional, Generic

from pydantic import BaseModel
from typing import TypeVar

T = TypeVar("T")


class ResponseEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S")
        elif isinstance(obj, float):
            return round(obj, 3)
        elif isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, BaseModel):
            return obj.dict()
        return JSONEncoder.default(self, obj)


class AppResponse(BaseModel, Generic[T]):
    http_code: int = 200
    err_code: int = 0
    message: Optional[str] = None
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"Response(err_code={self.err_code}, message={self.message})"

    def dict(self, *_, **__):
        return {"code": self.err_code, "message": self.message or "", "data": self.data}


class GlobalResponse(Exception):
    """支持全局Raise Response 参数设置"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        if len(args) > 0 and isinstance(args[0], str):
            kwargs.update({"message": args[0]})
        self.data: AppResponse = IllegalArgumentResponse(**kwargs)

    def __new__(cls, *args, **kwargs):
        obj = Exception.__new__(cls)
        return obj

    def __repr__(self):
        return self.data.__repr__()

    def __str__(self):
        return self.__repr__()


class IllegalArgumentResponse(AppResponse):
    """常规的请求参数有误/不合法"""

    err_code: int = 400
    message: Optional[str] = "请求参数有误"


class UnprocessableEntityResponse(AppResponse):
    """请求参数/格式与类型都正确，但是无法完成处理请求"""

    err_code: int = 422
    message: Optional[str] = "请求处理失败"
