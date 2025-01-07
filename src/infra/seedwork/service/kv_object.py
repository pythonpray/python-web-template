import enum
from typing import Optional, Callable, Any

from pydantic import BaseModel


class BaseEnum(enum.Enum):
    @classmethod
    def get_by_value(cls, value: Any):
        try:
            return cls(value.value if isinstance(value, BaseEnum) else value)
        except ValueError:
            return None

    @classmethod
    def get_by_name(cls, name):
        try:
            return cls[name.name if isinstance(name, BaseEnum) else name]
        except KeyError:
            return None

    def __eq__(self, other):
        return self.value == other or super(BaseEnum, self).__eq__(other)

    def __hash__(self):
        return hash(self.value)

    def translate(self, *args, **kwargs):
        return self.value


class BaseKvObject(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_dict(
        cls, d: Optional[dict], adapter: Optional[Callable[[dict], dict]] = None
    ):
        if d is None:
            return None
        if adapter:
            d = adapter(d)
        kwargs = {k: d.get(k) for k, _ in cls.schema()["properties"].items()}
        return cls(**kwargs)

    def to_dict(self):
        return self.dict()
