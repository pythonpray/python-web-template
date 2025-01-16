from sqlalchemy import Column, Integer, String, ForeignKey

from src.infra.seedwork.repo.model_base import BasicModel


class Enrollment(BasicModel):
    student_id = Column(Integer, ForeignKey("student.id"))
    course_id = Column(Integer, ForeignKey("course.id"))
    status = Column(String(20), default="enrolled")
