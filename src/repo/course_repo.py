from typing import List, Optional

from sqlalchemy import and_

from src.infra.seedwork.repo.repositories import BaseRepo
from src.repo.models.course import Course


class CourseRepository(BaseRepo):
    def __init__(self, session):
        super().__init__(session)

    @property
    def model_class(self):
        return Course

    def get_available_courses(self) -> List[Course]:
        return self.session.query(Course).filter(and_(Course.is_deleted.is_(False), Course.current_students < Course.max_students)).all()

    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        return self.session.query(Course).filter(and_(Course.id == course_id, Course.is_deleted.is_(False))).first()

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
