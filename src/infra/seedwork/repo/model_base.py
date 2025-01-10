import datetime
import logging
from typing import TypeVar

from sqlalchemy import Column, BigInteger, DateTime, func, BOOLEAN
from sqlalchemy.orm import declared_attr
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)


class CustomMixin:
    create_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(BOOLEAN, default=False, nullable=False)


# @as_declarative()
class Basic(CustomMixin):
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment="主键ID", index=True)

    @declared_attr
    def __tablename__(cls) -> str:
        """table名 默认 类名小写"""
        return cls.__name__.lower()

    def set_data(self, data: dict):
        """设置对象的属性"""
        # fields = [column.key for column in inspect(self.__class__).attrs]
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        setattr(self, "updated_at", datetime.datetime.now())
        # if k in fields and v != getattr(self, k):

    # @classmethod
    # def from_dict(cls, data: dict):
    #     return cls(**data)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self) -> str:
        return self.__str__()


BasicModel = declarative_base(cls=Basic)

M = TypeVar("M", bound=BasicModel)
