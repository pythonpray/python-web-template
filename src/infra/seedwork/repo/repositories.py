import asyncio
from abc import ABCMeta, abstractmethod
from functools import wraps
from typing import Generic, List, TypeVar, Type, Optional, Dict

from sqlalchemy import select, inspect, update, delete

from src.infra.seedwork.repo.models import BasicModel
from src.infra.seedwork.service.entities import BaseEntity


ModelType = TypeVar('ModelType', bound=BasicModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseEntity)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseEntity)


def ensure_sync(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if asyncio.iscoroutine(self.session):
            raise ValueError("Function must be called with a sync session object")
        return func(self, *args, **kwargs)

    return wrapper


class BaseSQLAlchemy(metaclass=ABCMeta):
    def __init__(self, session=None):
        self.session = session

    @staticmethod
    def _pure_attr(data: Dict, model_class: Type[BasicModel]):
        mapper = inspect(model_class)
        fields = [column.key for column in mapper.attrs]
        for k, v in data.copy().items():
            if k not in fields:
                data.pop(k)
        return data

    def sync_get(self, _id: int) -> ModelType:
        ...

    def sync_gets(self, where_condition, order_by=None, offset=0, limit=10) -> List[Optional[ModelType]]:
        ...

    def sync_update(self, obj_in: UpdateSchema) -> ModelType:
        ...

    async def gets(self, where_condition, order_by=None, offset=0, limit=10) -> List[Optional[ModelType]]:
        ...

    async def get_by_id(self, _id: int, ) -> ModelType:
        ...

    async def create(self, obj_in: CreateSchema) -> ModelType:
        ...

    async def update(self, obj_in: UpdateSchema) -> ModelType:
        ...

    async def delete(self, _id: int) -> None:
        ...

    async def count(self) -> int:
        ...


class BaseRepo(BaseSQLAlchemy, Generic[ModelType, CreateSchema, UpdateSchema]):

    @property
    @abstractmethod
    def model_class(self) -> Type[BasicModel]:
        ...

    # 查询、新增 返回值都是实体类，基于pydantic的，不需要再从db_model转换成pydantic.BaseModel 或者dataclass
    # 且当前实体类中的字段与db_model中的字段是一一对应，实体类可直接使用 <ModelEntity.属性名> 获取属性
    # 实体类继承关系 BaseModel(pydantic) <- BaseEntity <- 各个子ModelEntity(entity_class)
    @property
    def entity_class(self) -> Type[BaseEntity]:
        return type(self.model_class.__name__ + "Entity", (BaseEntity,), {})

    @property
    def get_primary_keys(self):
        return self.model_class.__table__.primary_key.columns.keys()

    def sync_entity_to_model(
            self,
            entity: BaseEntity,
            model_class: Type[BasicModel],
    ) -> Optional[BasicModel]:
        params = [getattr(entity, key, None) for key in self.get_primary_keys]
        model = self.session.get(model_class, params)
        if model:
            model.set_data(entity.raw_data)
            return model

    async def entity_to_model(
            self,
            entity: BaseEntity,
            model_class: Type[BasicModel],
    ) -> Optional[BasicModel]:
        params = [getattr(entity, key, None) for key in self.get_primary_keys]
        model = await self.session.get(model_class, params)
        if model:
            model.set_data(entity.raw_data)
            return model

        data = self._pure_attr(entity.raw_data, model_class)
        return model_class(**data)

    @ensure_sync
    def sync_get_by_id(self, _id: int) -> BaseEntity:  # 不一定是id，可以是primary_key/unique_key column
        result = self.session.get(self.model_class, _id)
        return self.entity_class.from_dict(result.raw_data) if result else None

    @ensure_sync
    def sync_gets(self, where_condition, order_by=None, offset=0, limit=None) -> List[BaseEntity]:
        stmt = select(self.model_class).where(where_condition)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        if limit:
            stmt = stmt.offset(offset).limit(limit)
        result = self.session.execute(stmt).scalars().all()
        return [self.entity_class.from_dict(i.raw_data) for i in result]

    @ensure_sync
    def sync_update(self, obj_in: UpdateSchema) -> ModelType:
        # 支持新增和修改
        model = self.sync_entity_to_model(obj_in, self.model_class)
        if not model:
            data = self._pure_attr(obj_in.raw_data, self.model_class)
            model = self.model_class(**data)
            self.session.add(model)

        self.session.flush([model])
        return self.entity_class.from_dict(model.raw_data)

    async def gets(self, where_condition, order_by=None, offset=0, limit=None) -> List[BaseEntity]:
        stmt = select(self.model_class).where(where_condition)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        if limit:
            stmt = stmt.offset(offset).limit(limit)
        result = (await self.session.execute(stmt)).scalars().all()
        return [self.entity_class.from_dict(i.raw_data) for i in result]

    async def get_by_id(self, _id: int) -> BaseEntity:  # 不一定是id，可能primary_key/unique_key column
        result = await self.session.get(self.model_class, _id)
        return self.entity_class.from_dict(result.raw_data) if result else None

    async def create(self, obj_in: CreateSchema) -> BaseEntity:
        """Create  需要手动commit"""
        data = self._pure_attr(obj_in.raw_data, self.model_class)
        model = self.model_class(**data)
        self.session.add(model)
        await self.session.flush([model])
        return self.entity_class.from_dict(model.raw_data)

    # todo 如果entity或者model中有func对象 不要使用该方法，调用flush有坑(lazy load)，手动在repo写stmt，使用await session.execute,
    async def update(self, obj_in: UpdateSchema) -> ModelType:
        """Update 需要手动commit"""
        model = await self.entity_to_model(obj_in, self.model_class)
        if not model:
            raise ValueError(f"{self.model_class.__name__} cant not found by primary key")

        await self.session.flush([model])
        return self.entity_class.from_dict(model.raw_data)

    async def delete(self, _id: int) -> None:
        """Delete 需要手动commit"""
        if getattr(self.model_class, "enable1", None):
            stmt = update(self.model_class).where(self.model_class.id == _id).values(enable=False)
            await self.session.execute(stmt)
        else:
            await self.session.execute(delete(self.model_class).where(self.model_class.id == _id))
