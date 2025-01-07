from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from repo.course_repo import CourseRepository, StudentRepository, EnrollmentRepository
from repo.models import Course, Enrollment


class CourseService:
    def __init__(self, session: Session):
        self.session = session
        self.course_repo = CourseRepository(session)
        self.student_repo = StudentRepository(session)
        self.enrollment_repo = EnrollmentRepository(session)

    def get_available_courses(self) -> List[Course]:
        return self.course_repo.get_available_courses()

    def get_student_courses(self, student_id: int) -> List[Course]:
        enrollments = self.enrollment_repo.get_student_enrollments(student_id)
        return [enrollment.course for enrollment in enrollments]

    def enroll_course(self, student_id: int, course_id: int) -> Enrollment:
        # 验证学生是否存在
        student = self.student_repo.get_student_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # 验证课程是否存在且有空位
        course = self.course_repo.get_course_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        if course.current_students >= course.max_students:
            raise HTTPException(status_code=400, detail="Course is full")

        # 检查是否已经选过这门课
        if self.enrollment_repo.is_student_enrolled(student_id, course_id):
            raise HTTPException(status_code=400, detail="Already enrolled in this course")

        # 创建选课记录
        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id,
            status="enrolled"
        )
        self.enrollment_repo.create(enrollment)
        
        # 更新课程当前学生数
        self.course_repo.increment_student_count(course_id)
        
        return enrollment

    def drop_course(self, student_id: int, course_id: int):
        enrollment = self.enrollment_repo.get_enrollment(student_id, course_id)
        if not enrollment or enrollment.status != "enrolled":
            raise HTTPException(status_code=404, detail="Enrollment not found")

        enrollment.status = "dropped"
        self.enrollment_repo.update(enrollment)
        
        # 更新课程当前学生数
        self.course_repo.decrement_student_count(course_id)
