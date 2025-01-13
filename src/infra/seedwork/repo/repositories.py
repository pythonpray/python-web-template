import abc
from abc import abstractmethod
from typing import Generic, List, TypeVar, Type, Optional, Dict, Any

from sqlalchemy import select, update, delete, and_
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import class_mapper, selectinload, noload

from src.infra.request_context import transaction
from infra.seedwork.repo.model_base import BasicModel
from src.infra.seedwork.domain.entities import BaseEntity


ModelType = TypeVar("ModelType", bound=BasicModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseEntity)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseEntity)


class BaseSQLAlchemy(abc.ABC):
    def __init__(self, session=None):
        self.session = session

    @staticmethod
    def _pure_attr(data: Dict, model_class: Type[BasicModel]):
        # 有些简单的创建/更新逻辑,前端传了多的无用参数,直接放在model_class(**data)会抛异常,添加过滤层
        mapper = class_mapper(model_class)
        return {k: v for k, v in data.items() if k in mapper.attrs.keys()}

    async def gets(self, where_condition, order_by=None, offset=0, limit=10) -> List[Optional[ModelType]]: ...

    async def get_by_id(
        self,
        _id: int,
    ) -> ModelType: ...

    async def create(self, obj_in: CreateSchema) -> ModelType: ...

    async def update(self, obj_in: UpdateSchema) -> ModelType: ...

    async def delete(self, _id: int) -> None: ...

    async def count(self) -> int: ...


class BaseRepo(BaseSQLAlchemy, Generic[ModelType, CreateSchema, UpdateSchema]):
    """
    BaseRepo 基类
        具体的业务repo字段继承了该类后,不需要在实现基础的查询,只需要在自己的repo子类中实现一些复杂查询即可,减少冗余代码
        百分之90的业务场景都是查询is_deleted=False的,所以这里的基础查询默认实现了这个逻辑
        delete默认逻辑删除,即标记is_deleted=True
    重要:
        个人意见在所有的model定义中,都是不推荐用relationship字段,虽然会让你写查询的时候语法更简单,实际上数据库该触发的查询一次也不会少,并且,在后续的关系维护中非常容易遗漏,或者更新时候约束报错,数据库的脏数据变得难以处理.
        还在是在数据库的层面增加关联字段,更新的时候显式的手动进行管理,更为安全,真出问题也易于排查.
        所以
        这里的session是用的async session, sqlalchemy orm 2.0中对异步session中有一些功能默认使用lazy load 比如 func.xxxx() 或者relationship的字段声明
        而BaseRepo其中一部分优化逻辑是把orm对象转换成pydantic model对象,做数据隔离, 那么会导致 涉及到func或者relationship查询的时候,lazy load不会直接拿到结果,而是在真正使用的地方做2次查询
        也就会在orm-> entity的过程中,要么报错,要么需要手动load,触发二次查询才可以,这里我选择不使用relationship, 也不去判断用户实际上是否需要关联字段的数据.而会造成不必要的查询.
        BaseRepo中的封装好的查询,只涉及简单查询,
        当然func不是不能用,如涉及使用,请在BaseRepo的子类中自己写stmt,await self.session.execute(stmt)来实现

    example:
        class StudentRepository(BaseRepo):
            def __init__(self, session: AsyncSession):
                super().__init__(session)

            @property
            def model_class(self) -> Type[Student]:
                return Student

            async def get_student_by_email(self, email: str) -> Optional[Student]:
                # 选其一
                return await self.session.gets(and_(Student.email == email, Student.name.like("%"+ "ha"))
                return await self.session.gets(and_(Student.email == email, Student.is_deleted.is_(False)), order_by=Student.created_at.desc(), limit=10, filter_is_deleted=False)

            async def get_student_by_id(self, student_id: int) -> Optional[Student]:
                return await self.session.get_by_id(student_id)

            async def create_student(self, student_instance) -> Student:
                # student_instance = Student(name=name, email=email) 可以是 sqlalchemy orm model类
                # student_instance = BaseEntity(name=name, email=email) 也可以是api请求传递过来的pydantic模型[BaseEntity继承了pydantic.BaseModel]
                return await self.session.create(student_instance)

    use example:
        repo = StudentRepository(session)
        ret = await repo.get_student_by_email(email)
        或者
        async with StudentRepository(session) as repo:
            ret = await repo.get_student_by_email(email)

        # 复合查询
        async def get_partition_usage_top_ten(self, workspace_id, start_date=None, end_date=None):
            stmt = (
                (
                    select(
                        FileInfoModel.partition_id,
                        PartitionModel.partition_name,
                        func.sum(FileInfoModel.deduct_points).label("value"))
                    .join(PartitionModel, FileInfoModel.partition_id == PartitionModel.partition_id)
                    .where(
                        and_(
                            FileInfoModel.create_time.between(start_date, end_date),
                            PartitionModel.workspace_id == workspace_id)
                    )
                    .group_by(
                        FileInfoModel.partition_id,
                        PartitionModel.partition_name)
                )
                .order_by(desc("value"))
                .limit(10)
            )
            result = await self.session.execute(stmt)
            return result.mappings().all()

    注:
        虽然说get_by_id实现了加载relationship字段的功能,但其实在所有的model定义中,都是不推荐用relationship字段[个人拙见]
    """

    @property
    @abstractmethod
    def model_class(self) -> Type[BasicModel]: ...

    @property
    def entity_class(self) -> Type[BaseEntity]:
        """
        这一步的作用是要避免应用层的代码直接对数据库对象进行操作的风险,数据库查出来的数据, 直接被转换成pydantic模型,省去手动转换的繁琐代码
        查询、新增 返回值都是实体类，基于pydantic的，不需要手动再从db_model转换成pydantic.BaseModel 或者dataclass
        且当前实体类中的字段与db_model中的字段是一一对应，实体类可直接使用 <ModelEntity.属性名> 获取属性
        实体类继承关系 BaseModel(pydantic) <- BaseEntity <- 各个子ModelEntity(entity_class)
        """
        mapper = class_mapper(self.model_class)
        columns = {}
        for column in mapper.columns:
            try:
                python_type = column.type.python_type
            except NotImplementedError:
                # 如果类型没有实现 python_type，使用 Any
                python_type = Any

            if not column.nullable:
                columns[column.key] = python_type
            else:
                columns[column.key] = Optional[python_type]
        return type(self.model_class.__name__ + "Entity", (BaseEntity,), {"__annotations__": columns})  # noqa

    @property
    def get_primary_keys(self):
        # 为了兼容有些人创建的表没有id字段,而是自己设置的primary key
        return self.model_class.__table__.primary_key.columns.keys()  # noqa

    async def entity_to_model(
        self,
        entity: BaseEntity,
    ) -> Optional[BasicModel]:
        primary_keys = {key: getattr(entity, key, None) for key in self.get_primary_keys}
        model = await self.session.get(self.model_class, primary_keys)

        if model:
            model.set_data(entity.model_dump())
            return model

        data = self._pure_attr(entity.model_dump(), self.model_class)
        return self.model_class(**data)

    async def gets(self, where_condition, order_by=None, offset=0, limit=None, filter_is_deleted=True) -> List[BaseEntity]:
        if filter_is_deleted:
            where_condition = and_(where_condition, self.model_class.is_deleted.is_(False))
        stmt = select(self.model_class).where(where_condition)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        if limit:
            stmt = stmt.offset(offset).limit(limit)
        result = (await self.session.execute(stmt)).scalars().all()
        return [self.entity_class.from_orm(i) for i in result]

    async def get_by_id(self, _id: int, load_relationships=False) -> BaseEntity:
        """
        load_relationships=False, 默认不去加载relationship的列
        """
        if load_relationships:
            stmt = select(self.model_class).options(noload("*")).where(self.model_class.id == _id)
            mapper = class_mapper(self.model_class)
            load_options = [
                selectinload(getattr(self.model_class, rel.key))
                for rel in mapper.relationships  # noqa
            ]
            if load_options:
                stmt = stmt.options(*load_options)
            result = (await self.session.execute(stmt)).scalar_one_or_none()
        else:
            result = await self.session.get(self.model_class, _id)  # lazy load 走缓存的query 效率更高
        a = self.entity_class.from_orm(result) if result else None
        return a

    @transaction
    async def create(self, obj_in: BasicModel | CreateSchema) -> BaseEntity:
        """支持传入 pydantic model[BaseEntity] 子类实例 或者 SQLAlchemy model[BasicModel] 实例"""
        if isinstance(obj_in, BasicModel):
            model = obj_in
        else:
            model = self.entity_to_model(obj_in)
        self.session.add(model)
        await self.session.flush([model])
        return self.entity_class.from_orm(model)

    # todo 如果entity或者model中有func对象 不要使用该方法，调用flush有坑(lazy load)，手动在repo写stmt，使用await session.execute,
    @transaction
    async def update(self, obj_in: UpdateSchema) -> ModelType:
        model = await self.entity_to_model(obj_in)
        if not model:
            raise ValueError(f"{self.model_class.__name__} cant not found by primary key")

        await self.session.flush([model])
        return self.entity_class.from_orm(model)

    @transaction
    async def delete(self, _id: int, logic=True) -> None:
        if logic:
            stmt = update(self.model_class).where(self.model_class.id == _id).values(is_deleted=True)
            await self.session.execute(stmt)
        else:
            await self.session.execute(delete(self.model_class).where(self.model_class.id == _id))

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value: str, exc_traceback: str) -> None:
        if exc_type is not None:
            await self.session.rollback()
            return

        try:
            await self.session.commit()
        except DatabaseError:
            await self.session.rollback()
            raise
