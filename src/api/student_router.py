from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.request_scheme.student_req import CreateStudentReq, UpdateStudentReq
from api.response_scheme.student_resp import StudentResp
from domain.course.service import CourseService
from src.infra.seedwork.repo.async_session import get_session

router = APIRouter(prefix="/user", tags=["users"])


@router.post("/students", response_model=StudentResp)
async def create_student(request: CreateStudentReq, session: AsyncSession = Depends(get_session)):
    """创建新学生"""
    service = CourseService(session)
    student = await service.create_student(name=request.name, email=str(request.email))
    return student


@router.get("/student/{student_id}", response_model=StudentResp)
async def get_student(student_id: int, session: AsyncSession = Depends(get_session)):
    service = CourseService(session)
    entity = await service.get_student(student_id)
    return entity


@router.put("/student", response_model=StudentResp)
async def update_student(params: UpdateStudentReq, session: AsyncSession = Depends(get_session)):
    service = CourseService(session)
    entity = await service.student_repo.update(params)
    return entity
