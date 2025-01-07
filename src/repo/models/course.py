from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.infra.seedwork.repo.models import BasicModel


class Course(BasicModel):
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    teacher = Column(String(100))
    max_students = Column(Integer, default=50)
    current_students = Column(Integer, default=0)

    enrollments = relationship("Enrollment", back_populates="course")
