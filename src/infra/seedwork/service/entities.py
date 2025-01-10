import logging
from typing import TypeVar

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class BaseScheme(BaseModel):
    """自定义的scheme 基类,代码库中service层的所有数据类都应该继承与此"""

    def to_dict(self, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = ["created_at", "updated_at", "is_deleted"]

        d = self.model_dump(exclude=exclude_fields)
        return d


class BaseEntity(BaseScheme):
    """从数据库orm模型转化出来的 数据entity类"""

    class Config:
        from_attributes = True
        extra = "allow"
        populate_by_name = True

        arbitrary_types_allowed = True
        # 验证赋值
        validate_assignment = False


E = TypeVar("E", bound=BaseEntity)
