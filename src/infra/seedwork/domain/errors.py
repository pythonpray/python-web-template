from pydantic import BaseModel


class AbortError(Exception):
    """用于全局异常消息捕获"""

    pass


class AbortResponse(BaseModel):
    message: str
    status_code: int
    err_code: int = 0


def abort(message: str, status_code: int = 422, *, err_code: int = 0):
    """支持全局消息上报，可以直接中断请求

    :param message: 返回的message
    :param status_code: 对应到 HTTP STATUS CODE
    :param err_code: 业务错误码
    """
    status_code = 200 if err_code else status_code  # 前端判断业务err_code时，http code 只允许2xx
    response = AbortResponse(message=message, status_code=status_code, err_code=err_code)
    raise AbortError(response)


class BaseDomainError(Exception):
    def __init__(self, err_code: int, message: str, **kwargs):
        super().__init__(**kwargs)
        self.err_code = err_code
        self.message = message
