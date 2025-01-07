from typing import Optional

from sqlalchemy import and_

from src.infra.seedwork.repo.repositories import BaseRepo
from src.repo.models.student import Student


class StudentRepository(BaseRepo):
    def __init__(self, session):
        super().__init__(session)

    @property
    def model_class(self):
        return Student

    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        return self.session.query(Student).filter(and_(Student.id == student_id, Student.is_deleted.is_(False))).first()
