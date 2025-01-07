import json
import logging
from typing import TypeVar, Any, Dict, List

from sqlalchemy import inspect, JSON, Column, BigInteger, DateTime, func, BOOLEAN
from sqlalchemy.orm import as_declarative, declared_attr

logger = logging.getLogger(__name__)


class TimestampMixin(object):
    create_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(BOOLEAN, default=False, nullable=False)


@as_declarative()
class BasicModel(TimestampMixin):
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment="主键ID", index=True)

    @declared_attr
    def __tablename__(cls) -> str:
        """table名 默认 类名小写"""
        return cls.__name__.lower()

    @property
    def raw_data(self) -> Dict[str, Any]:
        """获取对象的所有属性"""
        return {column.key: getattr(self, column.key) for column in inspect(self.__class__).attrs}

    @property
    def json_columns(self) -> List[str]:
        """获取JSON类型的列"""
        return [column.key for column in inspect(self.__class__).attrs if column.expression is not None and isinstance(column.expression.type, JSON)]

    def set_data(self, data: dict):
        """设置对象的属性"""
        fields = [column.key for column in inspect(self.__class__).attrs]
        for k, v in data.items():
            if k in fields and v != getattr(self, k):
                setattr(self, k, v)

    def __setattr__(self, key: str, value: Any):
        """设置属性时的钩子，用于处理JSON数据"""
        if hasattr(self, 'json_columns'):
            if isinstance(value, (list, dict)) and key not in self.json_columns:
                value = json.dumps(value, ensure_ascii=False)
        super().__setattr__(key, value)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {"id": self.id}

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self) -> str:
        return self.__str__()


M = TypeVar("M", bound=BasicModel)
