from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain.course.course_repo import CourseRepository
from domain.course.enrollment_repo import EnrollmentRepository
from infra.models.course import Course
from infra.models.enrollments import Enrollment
from infra.models.student import Student
from domain.user.student_repo import StudentRepository
from infra.seedwork.domain.scheme import BaseEntity


class CourseService:
    """domain的业务层,也就是domain对其他业务提供的调用入口,比如其他domain的调用
    domain的组成,是有modules和repo组成.
        repo主要涉及数据库的curd
        modules 数据库无关的 业务封装模块
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.course_repo = CourseRepository(session)
        self.student_repo = StudentRepository(session)
        self.enrollment_repo = EnrollmentRepository(session)

    async def create_course(self, name: str, max_students: int) -> BaseEntity:
        """创建新课程"""
        course = Course(name=name, max_students=max_students, current_students=0)
        return await self.course_repo.create(course)

    async def create_student(self, name: str, email: str) -> BaseEntity:
        """创建新学生"""
        # 检查邮箱是否已被使用
        existing_student = await self.student_repo.get_student_by_email(email)
        if existing_student:
            raise HTTPException(status_code=400, detail="Email already registered")

        student = Student(name=name, email=email)
        return await self.student_repo.create(student)

    async def list_students(self) -> List[BaseEntity]:
        return await self.student_repo.gets(where_condition=Student.is_deleted.is_(False))

    async def get_student(self, student_id: int) -> BaseEntity:
        return await self.student_repo.get_by_id(student_id)

    async def get_available_courses(self) -> List[BaseEntity]:
        return await self.course_repo.get_available_courses()

    async def get_student_courses(self, student_id: int) -> List[BaseEntity]:
        # 检查学生是否存在
        student = await self.student_repo.get_student_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # 获取学生的所有选课记录
        enrollments = await self.enrollment_repo.get_student_enrollments(student_id)

        # 获取所有相关课程
        courses = []
        for enrollment in enrollments:
            course = await self.course_repo.get_course_by_id(enrollment.course_id)
            if course:
                courses.append(course)
        return courses

    async def enroll_course(self, student_id: int, course_id: int) -> Enrollment:
        # 检查学生是否存在
        student = await self.student_repo.get_student_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # 检查课程是否存在且有空位
        course = await self.course_repo.get_course_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        if course.current_students >= course.max_students:
            raise HTTPException(status_code=400, detail="Course is full")

        # 检查是否已经选过这门课
        if await self.enrollment_repo.is_student_enrolled(student_id, course_id):
            raise HTTPException(status_code=400, detail="Already enrolled in this course")

        # 创建选课记录
        enrollment = Enrollment(student_id=student_id, course_id=course_id, status="enrolled")
        await self.enrollment_repo.create(enrollment)

        # 更新课程当前学生数
        await self.course_repo.increment_student_count(course_id)

        return enrollment

    async def drop_course(self, student_id: int, course_id: int):
        enrollment = await self.enrollment_repo.get_enrollment(student_id, course_id)
        if not enrollment or enrollment.status != "enrolled":
            raise HTTPException(status_code=404, detail="Enrollment not found")

        enrollment.status = "dropped"
        await self.enrollment_repo.update(enrollment)

        # 更新课程当前学生数
        await self.course_repo.decrement_student_count(course_id)

    async def get_course_students(self, course_id: int) -> List[BaseEntity]:
        """获取课程的所有在读学生"""
        # 检查课程是否存在
        course = await self.course_repo.get_course_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # 获取课程的所有选课记录
        enrollments = await self.enrollment_repo.get_course_enrollments(course_id)

        # 获取所有相关学生
        students = []
        for enrollment in enrollments:
            if enrollment.status == "enrolled":  # 只返回在读学生
                student = await self.student_repo.get_student_by_id(enrollment.student_id)
                if student:
                    students.append(student)
        return students
