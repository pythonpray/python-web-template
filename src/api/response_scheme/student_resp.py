from src.infra.seedwork.api.api_base_scheme import RespScheme


class StudentResp(RespScheme):
    name: str
    email: str


class CourseResp(RespScheme):
    id: int
    name: str
    max_students: int
    current_students: int
