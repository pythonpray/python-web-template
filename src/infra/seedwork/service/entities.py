import json
import logging
from typing import TypeVar, List, Any, Dict

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class BaseEntity(BaseModel):  # todo 跟模型字段对应的 数据类建议继承BaseEntity
    raw_data: Dict[str, Any] = {}

    def __init__(self, **data):
        super().__init__(**data)
        self.update_data(**self.model_dump(exclude={"raw_data"}))

    @property
    def json_fields(self) -> List[str]:
        return []

    def _decode_value(self, field_name: str, value: Any) -> Any:
        if field_name in self.json_fields:
            if value and isinstance(value, str):
                try:
                    value = json.loads(value)
                except (TypeError, ValueError):
                    value = None
        return value

    def __getattr__(self, name):
        if name in self.raw_data:
            value = self.raw_data[name]
            value = self._decode_value(name, value) or value
            return value
        try:
            return super().__getattr__(name)
        except AttributeError:
            return None

    def __setattr__(self, key, value):
        if key in self.raw_data:
            value = self._decode_value(key, value)
            self.raw_data[key] = value

        super().__setattr__(key, value)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def update_data(self, **kwargs):
        self.raw_data.update(kwargs)

    def to_dict(self, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = ["created_at", "updated_at", "is_deleted"]

        d = {
            field: getattr(self, field)
            for field in self.raw_data
            if field not in exclude_fields
        }

        for field_name in self.json_fields:
            d[field_name] = self.__getattr__(field_name)
        return d

    @classmethod
    def from_dict(cls, data: dict, **kwargs):
        return cls(
            raw_data={
                k: v for k, v in data.items() if isinstance(k, str)
            },
            **kwargs
        )


E = TypeVar("E", bound=BaseEntity)
