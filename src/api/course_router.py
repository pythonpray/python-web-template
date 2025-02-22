from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from domain.course.service import CourseService
from api.request_scheme.student_req import CreateCourseReq
from api.response_scheme.student_resp import CourseResp, StudentResp
from infra.logger import app_logger
from infra.seedwork.repo.async_session import get_session
from utils.app_response import ResponseHandler, AppResponse


router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/create", response_model=AppResponse[CourseResp])
async def create_course(request: CreateCourseReq, session: AsyncSession = Depends(get_session)):
    """创建新课程"""
    app_logger.info(f"Creating new course: {request.name}")
    service = CourseService(session)
    course = await service.create_course(name=request.name, max_students=request.max_students)
    app_logger.info(f"Course created successfully: {course.id}")
    return ResponseHandler.success(course)


@router.get("/available", response_model=AppResponse[List[CourseResp]])
async def get_available_courses(session: AsyncSession = Depends(get_session)):
    app_logger.info("Fetching available courses")
    service = CourseService(session)
    courses = await service.get_available_courses()
    app_logger.info(f"Found {len(courses)} available courses")
    return ResponseHandler.success(courses)


@router.get("/student/{student_id}", response_model=AppResponse[List[CourseResp]])
async def get_student_courses(student_id: int, session: AsyncSession = Depends(get_session)):
    """获取学生已选课程列表"""
    app_logger.info(f"Fetching courses for student {student_id}")
    service = CourseService(session)
    courses = await service.get_student_courses(student_id)
    app_logger.info(f"Found {len(courses)} courses for student {student_id}")
    return ResponseHandler.success(courses)


@router.get("/{course_id}/students", response_model=AppResponse[List[StudentResp]])
async def get_course_students(course_id: int, session: AsyncSession = Depends(get_session)):
    """获取课程已选学生列表"""
    app_logger.info(f"Fetching students for course {course_id}")
    service = CourseService(session)
    students = await service.get_course_students(course_id)
    app_logger.info(f"Found {len(students)} students in course {course_id}")
    return ResponseHandler.success(students)


@router.post("/{course_id}/enroll/{student_id}", response_model=AppResponse)
async def enroll_course(course_id: int, student_id: int, session: AsyncSession = Depends(get_session)):
    app_logger.info(f"Enrolling student {student_id} in course {course_id}")
    service = CourseService(session)
    await service.enroll_course(student_id, course_id)
    app_logger.info(f"Student {student_id} successfully enrolled in course {course_id}")
    return ResponseHandler.success(message="Successfully enrolled in course")


@router.post("/{course_id}/drop/{student_id}", response_model=AppResponse)
async def drop_course(course_id: int, student_id: int, session: AsyncSession = Depends(get_session)):
    app_logger.info(f"Dropping student {student_id} from course {course_id}")
    service = CourseService(session)
    await service.drop_course(student_id, course_id)
    app_logger.info(f"Student {student_id} successfully dropped from course {course_id}")
    return ResponseHandler.success(message="Successfully dropped course")
