from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.infra.seedwork.repo.models import BasicModel


class Student(BasicModel):
    """
    table name  默认是 类名小写
    默认有 id is_deleted created_at updated_at 4个字段 已经在基类中声明过了
    只需要关心业务字段即可
    """

    name = Column(String(100), nullable=False)
    student_id = Column(String(20), unique=True, nullable=False)
    email = Column(String(100))

    enrollments = relationship("Enrollment", back_populates="student")