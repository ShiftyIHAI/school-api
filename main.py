from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from starlette.status import HTTP_404_NOT_FOUND

from database import get_db
from models import Student, Instructor, Course
from schemas import CreateStudentRequest, CreateStudentResponse, CreateInstructorRequest, CreateInstructorResponse, CreateCourseRequest, CreateCourseResponse


app = FastAPI()

#students
@app.get("/students")
async def get_students(db: Session = Depends(get_db)) -> list[Student]:
    return db.exec(select(Student)).all()


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(new_student: CreateStudentRequest, db: Session = Depends(get_db)) -> CreateStudentResponse:
    student = Student(**new_student.model_dump())
    db.add(student)
    db.commit()
    return CreateStudentResponse(student_id=student.student_id)


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    student: Student | None = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found!")
    db.delete(student)
    db.commit()


#instructors
@app.get("/instructors")
async def get_instructors(db: Session = Depends(get_db)) -> list[Instructor]:
    return db.exec(select(Instructor)).all()


@app.get("/instructors/{id}/courses")
async def get_instructors_courses(id: int, db: Session = Depends(get_db)) -> list[str]:
    instructor: Instructor | None = db.get(Instructor, id)
    if instructor is None:
        raise HTTPException(status_code=404, detail=f"Instructor with ID {id} not found!")
    return [course.title for course in instructor.courses]
    #course_names: list[str] = []
    #for i in range(len(instructor.courses)):
    #    course_names.append(instructor.courses[i].title)
    #return course_names


@app.post("/instructors", status_code=status.HTTP_201_CREATED)
async def create_instructor(new_instructor: CreateInstructorRequest, db: Session = Depends(get_db)) -> CreateInstructorResponse:
    instructor = Instructor(**new_instructor.model_dump())
    db.add(instructor)
    db.commit()
    return CreateInstructorResponse(id=instructor.id)


@app.delete("/instructors/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instructor(id: int, db: Session = Depends(get_db)):
    instructor: Instructor | None = db.get(Instructor, id)
    if instructor is None:
        raise HTTPException(status_code=404, detail=f"Instructor with ID {id} not found!")
    db.delete(instructor)
    db.commit()


#courses
@app.get("/courses")
async def get_courses(db: Session = Depends(get_db)) -> list[Course]:
    return db.exec(select(Course)).all()


@app.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_course(new_course: CreateCourseRequest, db: Session = Depends(get_db)) -> CreateCourseResponse:
    course = Course(**new_course.model_dump())
    db.add(course)
    db.commit()
    return CreateCourseResponse(course_id=course.course_id)


@app.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    course: Course | None = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found!")
    db.delete(course)
    db.commit()
