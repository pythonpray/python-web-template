from pydantic import Field

from infra.seedwork.api.api_base_scheme import RequestScheme
# 所有的RequestScheme 都用Field加上校验 或者用field_validator 自定义校验,省去了业务代码中的各种判断


class StudentReq(RequestScheme):
    id: int
    name: str = Field(..., min_length=2, max_length=100, description="名称")
    email: str = Field(..., min_length=7, max_length=20, description="email")


class CourseReq(RequestScheme):
    id: int
    name: str = Field(..., min_length=2, max_length=100, description="名称")
    max_students: int
    current_students: int


class CreateCourseReq(RequestScheme):
    name: str
    max_students: int


class CreateStudentReq(RequestScheme):
    name: str = Field(..., min_length=2, max_length=100, description="名称")
    email: str = Field(..., min_length=7, max_length=20, description="email")


class UpdateStudentReq(CreateStudentReq):
    id: int
