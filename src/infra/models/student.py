from sqlalchemy import Column, String

# 需要特别注意的是 这里导入要用from src.xxx导入, 否则alembic检查不到模型变化
from src.infra.seedwork.repo.model_base import BasicModel


class Student(BasicModel):
    """
    table name  默认是 类名小写
    默认有 id is_deleted created_at updated_at 4个字段 已经在基类中声明过了
    只需要关心业务字段即可
    """

    name = Column(String(100), nullable=False, comment="姓名")
    email = Column(String(255), nullable=False, unique=True, comment="邮箱")
