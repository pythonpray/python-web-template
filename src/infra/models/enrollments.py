from sqlalchemy import Column, Integer, String, ForeignKey

from infra.seedwork.repo.model_base import BasicModel


class Enrollment(BasicModel):
    student_id = Column(Integer, ForeignKey("student.id"))
    course_id = Column(Integer, ForeignKey("course.id"))
    status = Column(String(20), default="enrolled")  # enrolled, dropped

    # student = relationship("Student", back_populates="enrollments")
    # course = relationship("Course", back_populates="enrollments")
