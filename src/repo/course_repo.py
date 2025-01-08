from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.seedwork.repo.repositories import BaseRepo
from src.repo.models.course import Course


class CourseRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    @property
    def model_class(self):
        return Course

    async def get_available_courses(self) -> List[Course]:
        query = select(Course).where(and_(Course.is_deleted.is_(False), Course.current_students < Course.max_students))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_course_by_id(self, course_id: int) -> Optional[Course]:
        query = select(Course).where(and_(Course.id == course_id, Course.is_deleted.is_(False)))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def increment_student_count(self, course_id: int):
        course = await self.get_course_by_id(course_id)
        if course:
            course.current_students += 1
            await self.session.commit()

    async def decrement_student_count(self, course_id: int):
        course = await self.get_course_by_id(course_id)
        if course and course.current_students > 0:
            course.current_students -= 1
            await self.session.commit()
