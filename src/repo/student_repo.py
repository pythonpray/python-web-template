from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.seedwork.repo.repositories import BaseRepo
from src.repo.models.student import Student


class StudentRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    @property
    def model_class(self):
        return Student

    async def get_student_by_id(self, student_id: int) -> Optional[Student]:
        query = select(Student).where(and_(Student.id == student_id, Student.is_deleted.is_(False)))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_student_by_email(self, email: str) -> Optional[Student]:
        """通过邮箱查找学生"""
        query = select(Student).where(and_(Student.email == email, Student.is_deleted.is_(False)))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
