from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.infra.seedwork.repo.models import BasicModel


class Enrollment(BasicModel):
    __tablename__ = "enrollments"

    student_id = Column(Integer, ForeignKey("student.id"))
    course_id = Column(Integer, ForeignKey("course.id"))
    status = Column(String(20), default="enrolled")  # enrolled, dropped

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")