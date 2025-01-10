from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.request_scheme.student_req import CreateStudentReq, UpdateStudentReq
from api.response_scheme.student_resp import StudentResp
from domain.course.application import CourseService
from src.infra.seedwork.repo.async_session import get_session
from utils.app_response import ResponseHandler, AppResponse

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/student/{student_id}", response_model=AppResponse[StudentResp])
async def get_student(student_id: int, session: AsyncSession = Depends(get_session)):
    service = CourseService(session)
    entity = await service.get_student(student_id)
    return ResponseHandler.success(entity)


@router.post("/student", response_model=AppResponse[StudentResp])
async def create_student(params: CreateStudentReq, session: AsyncSession = Depends(get_session)):
    service = CourseService(session)
    entity = await service.create_student(params.name, params.email)
    return ResponseHandler.success(entity)


@router.put("/student", response_model=AppResponse[StudentResp])
async def update_student(params: UpdateStudentReq, session: AsyncSession = Depends(get_session)):
    service = CourseService(session)
    entity = await service.student_repo.update(params)
    return ResponseHandler.success(entity)
