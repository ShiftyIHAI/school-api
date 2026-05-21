from pydantic import BaseModel


class CreateStudentRequest(BaseModel):
    first_name: str
    last_name: str
    email: str

class CreateStudentResponse(BaseModel):
    student_id: int


class CreateInstructorRequest(BaseModel):
    first_name: str
    last_name: str
    email: str

class CreateInstructorResponse(BaseModel):
    id: int

class CreateCourseRequest(BaseModel):
    instructor_id: int
    title: str
    course_number: str
    credits: int

class CreateCourseResponse(BaseModel):
    course_id: int
