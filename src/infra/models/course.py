from sqlalchemy import Column, Integer, String

from infra.seedwork.repo.model_base import BasicModel


class Course(BasicModel):
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    teacher = Column(String(100))
    max_students = Column(Integer, default=50)
    current_students = Column(Integer, default=0)
