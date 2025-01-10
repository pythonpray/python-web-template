from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.request_scheme.student_req import CreateStudentReq, UpdateStudentReq
from api.response_scheme.student_resp import StudentResp
from domain.course.application import CourseService
from src.infra.logger import app_logger
from src.infra.seedwork.repo.async_session import get_session
from utils.app_response import ResponseHandler, AppResponse

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/student/{student_id}", response_model=AppResponse[StudentResp])
async def get_student(student_id: int, session: AsyncSession = Depends(get_session)):
    app_logger.info(f"Fetching student with id: {student_id}")
    service = CourseService(session)
    entity = await service.get_student(student_id)
    app_logger.info(f"Found student: {entity.name}")
    return ResponseHandler.success(entity)


@router.post("/student", response_model=AppResponse[StudentResp])
async def create_student(params: CreateStudentReq, session: AsyncSession = Depends(get_session)):
    app_logger.info(f"Creating new student: {params.name}")
    service = CourseService(session)
    entity = await service.create_student(params.name, params.email)
    app_logger.info(f"Student created successfully: {entity.id}")
    return ResponseHandler.success(entity)


@router.put("/student", response_model=AppResponse[StudentResp])
async def update_student(params: UpdateStudentReq, session: AsyncSession = Depends(get_session)):
    app_logger.info(f"Updating student {params.id}")
    service = CourseService(session)
    entity = await service.student_repo.update(params)
    app_logger.info(f"Student {entity.id} updated successfully")
    return ResponseHandler.success(entity)
