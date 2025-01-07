from typing import List, Optional

from sqlalchemy import and_

from src.infra.seedwork.repo.repositories import BaseRepo
from src.repo.models.enrollments import Enrollment


class EnrollmentRepository(BaseRepo):
    def __init__(self, session):
        super().__init__(session)

    @property
    def model_class(self):
        return Enrollment

    def get_student_enrollments(self, student_id: int) -> List[Enrollment]:
        return (
            self.session.query(Enrollment)
            .filter(and_(Enrollment.student_id == student_id, Enrollment.is_deleted.is_(False), Enrollment.status == "enrolled"))
            .all()
        )

    def get_enrollment(self, student_id: int, course_id: int) -> Optional[Enrollment]:
        return (
            self.session.query(Enrollment)
            .filter(and_(Enrollment.student_id == student_id, Enrollment.course_id == course_id, Enrollment.is_deleted.is_(False)))
            .first()
        )

    def is_student_enrolled(self, student_id: int, course_id: int) -> bool:
        enrollment = self.get_enrollment(student_id, course_id)
        return enrollment is not None and enrollment.status == "enrolled"
