from src.infra.seedwork.api.api_base_scheme import RequestScheme


class StudentReq(RequestScheme):
    id: int
    name: str
    email: int


class CourseReq(RequestScheme):
    id: int
    name: str
    max_students: int
    current_students: int


class CreateCourseReq(RequestScheme):
    name: str
    max_students: int


class CreateStudentReq(RequestScheme):
    name: str
    email: str


class UpdateStudentReq(CreateStudentReq):
    id: int
