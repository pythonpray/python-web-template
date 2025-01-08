import functools
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import AsyncGenerator
from uuid import uuid4


class RequestContext:
    # 上下文变量
    request_id_ctx: ContextVar[str] = ContextVar("request_id")
    is_in_transaction_ctx: ContextVar[bool] = ContextVar("is_in_transaction", default=False)
    user_session_ctx: ContextVar[dict] = ContextVar("user_session", default={})


req_context = RequestContext()


@asynccontextmanager
async def request_context() -> AsyncGenerator:
    # 生成请求ID
    request_id = str(uuid4())
    request_token = req_context.request_id_ctx.set(request_id)

    try:
        yield req_context
    finally:
        # 清理上下文变量
        req_context.request_id_ctx.reset(request_token)
        req_context.user_session_ctx.set({})  # 重置用户会话
        req_context.is_in_transaction_ctx.set(False)  # 重置事务状态


def transaction(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if req_context.is_in_transaction_ctx.get():
            return f(*args, **kwargs)
        transaction_token = req_context.is_in_transaction_ctx.set(True)

        try:
            ret = f(*args, **kwargs)
            return ret
        except Exception as e:
            raise e
        finally:
            req_context.is_in_transaction_ctx.reset(transaction_token)

    return wrapper
