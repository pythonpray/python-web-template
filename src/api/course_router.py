from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request_scheme.student_req import CreateCourseReq
from src.api.response_scheme.student_resp import CourseResp
from src.infra.seedwork.repo.async_session import get_session
from domain.course.service import CourseService

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/create", response_model=CourseResp)
async def create_course(request: CreateCourseReq, session: AsyncSession = Depends(get_session)):
    """创建新课程"""
    service = CourseService(session)
    course = await service.create_course(name=request.name, max_students=request.max_students)
    return course


@router.get("/available", response_model=List[CourseResp])
async def get_available_courses(session: AsyncSession = Depends(get_session)):
    service = CourseService(session)
    return await service.get_available_courses()


@router.post("/{course_id}/enroll/{student_id}")
async def enroll_course(course_id: int, student_id: int, session: AsyncSession = Depends(get_session)):
    service = CourseService(session)
    await service.enroll_course(student_id, course_id)
    return {"message": "Successfully enrolled in course"}


@router.post("/{course_id}/drop/{student_id}")
async def drop_course(course_id: int, student_id: int, session: AsyncSession = Depends(get_session)):
    service = CourseService(session)
    await service.drop_course(student_id, course_id)
    return {"message": "Successfully dropped course"}
