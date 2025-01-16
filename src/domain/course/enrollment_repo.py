from typing import List, Optional, Type

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from infra.seedwork.repo.repositories import BaseRepo
from infra.models.enrollments import Enrollment


class EnrollmentRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    @property
    def model_class(self) -> Type[Enrollment]:
        return Enrollment

    async def get_student_enrollments(self, student_id: int) -> List[Enrollment]:
        query = select(Enrollment).where(and_(Enrollment.student_id == student_id, Enrollment.is_deleted.is_(False), Enrollment.status == "enrolled"))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_course_enrollments(self, course_id: int) -> List[Enrollment]:
        """获取课程的所有选课记录"""
        query = select(Enrollment).where(and_(Enrollment.course_id == course_id, Enrollment.is_deleted.is_(False), Enrollment.status == "enrolled"))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_enrollment(self, student_id: int, course_id: int) -> Optional[Enrollment]:
        query = select(Enrollment).where(and_(Enrollment.student_id == student_id, Enrollment.course_id == course_id, Enrollment.is_deleted.is_(False)))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def is_student_enrolled(self, student_id: int, course_id: int) -> bool:
        enrollment = await self.get_enrollment(student_id, course_id)
        return enrollment is not None and enrollment.status == "enrolled"
