from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from service.course_service import CourseService
from infra.database import get_db


router = APIRouter(prefix="/courses", tags=["courses"])


class CourseResponse(BaseModel):
    id: int
    name: str
    description: str
    teacher: str
    max_students: int
    current_students: int

    class Config:
        orm_mode = True


@router.get("/available", response_model=List[CourseResponse])
def get_available_courses(db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.get_available_courses()


@router.get("/student/{student_id}", response_model=List[CourseResponse])
def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.get_student_courses(student_id)


@router.post("/{course_id}/enroll/{student_id}")
def enroll_course(course_id: int, student_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    enrollment = service.enroll_course(student_id, course_id)
    return {"message": "Successfully enrolled in course"}


@router.post("/{course_id}/drop/{student_id}")
def drop_course(course_id: int, student_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    service.drop_course(student_id, course_id)
    return {"message": "Successfully dropped course"}
