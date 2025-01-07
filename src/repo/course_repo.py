from typing import List, Optional

from sqlalchemy import and_

from src.repo.models.course import Course

from src.repo.models.enrollments import Enrollment
from src.repo.models.student import Student

from src.infra.seedwork.repo.repositories import BaseRepo


class CourseRepository(BaseRepo):
    def __init__(self, session):
        super().__init__(session)

    @property
    def model_class(self):
        return Course

    def get_available_courses(self) -> List[Course]:
        return self.session.query(Course).filter(
            and_(
                Course.is_deleted == False,
                Course.current_students < Course.max_students
            )
        ).all()

    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        return self.session.query(Course).filter(
            and_(
                Course.id == course_id,
                Course.is_deleted == False
            )
        ).first()

    def increment_student_count(self, course_id: int):
        course = self.get_course_by_id(course_id)
        if course:
            course.current_students += 1
            self.session.commit()

    def decrement_student_count(self, course_id: int):
        course = self.get_course_by_id(course_id)
        if course and course.current_students > 0:
            course.current_students -= 1
            self.session.commit()


class StudentRepository(BaseRepository[Student]):
    def __init__(self, session: Session):
        super().__init__(Student, session)

    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        return self.session.query(Student).filter(
            and_(
                Student.id == student_id,
                Student.is_deleted == False
            )
        ).first()


class EnrollmentRepository(BaseRepository[Enrollment]):
    def __init__(self, session: Session):
        super().__init__(Enrollment, session)

    def get_student_enrollments(self, student_id: int) -> List[Enrollment]:
        return self.session.query(Enrollment).filter(
            and_(
                Enrollment.student_id == student_id,
                Enrollment.is_deleted == False,
                Enrollment.status == "enrolled"
            )
        ).all()

    def get_enrollment(self, student_id: int, course_id: int) -> Optional[Enrollment]:
        return self.session.query(Enrollment).filter(
            and_(
                Enrollment.student_id == student_id,
                Enrollment.course_id == course_id,
                Enrollment.is_deleted == False
            )
        ).first()

    def is_student_enrolled(self, student_id: int, course_id: int) -> bool:
        enrollment = self.get_enrollment(student_id, course_id)
        return enrollment is not None and enrollment.status == "enrolled"
