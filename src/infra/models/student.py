from sqlalchemy import Column, String

from infra.seedwork.repo.model_base import BasicModel


class Student(BasicModel):
    """
    table name  默认是 类名小写
    默认有 id is_deleted created_at updated_at 4个字段 已经在基类中声明过了
    只需要关心业务字段即可
    """

    name = Column(String(100), nullable=False, comment="姓名")
    email = Column(String(255), nullable=False, unique=True, comment="邮箱")
