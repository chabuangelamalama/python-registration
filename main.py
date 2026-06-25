
from fastapi import FastAPI
from pydantic import BaseModel
from database import create_table, add_student, get_students, add_teacher, get_teachers, add_course, get_courses



app = FastAPI()
create_table()

class Student(BaseModel):
    name: str
    age:int
    email:str
    country:str
    id_number:str 

class Teacher(BaseModel):
    name: str
    age: int
    email: str
    department: str
    employee_id:str

class Course(BaseModel):
    course_name: str
    course_code: str
    credits : int
    year: str
    trainer: str


    ### the Get section

@app.get("/")
def home():
    return{"message":"Welcome to my Api server"}

@app.get("/students")
def list_students():
    students = get_students()
    return students


@app.get("/teachers")
def list_teachers():
    teachers = get_teachers ()
    return teachers

@app.get("/course")
def list_courses():
    courses = get_courses()
    return courses

## the Post Section

@app.post("/students")
def register_student(student:Student):
    add_student(student.name,
                student.age, 
                student.email, 
                student.country, 
                student.id_number)
    return{"message": "Student Registered", "student":student  }

@app.post("/teachers")
def register_teacher(teacher:Teacher):
   add_teacher(
       teacher.name,
       teacher.age,
       teacher.email,
       teacher.department,
       teacher.employee_id
       
) 
   return{
    "message": "Teacher Registered",
    "teacher": teacher
}  
   
@app.post("/courses")
def register_course(course: Course):
       add_course(
           course.course_name,
           course.course_code,
           course.credits,
           course.year,
           course.trainer
       ) 
       return{"message": "Course ADDED ",
               "course": course}

@app.put("/student/{id}")
def update_student(id: int, student:Student):
       update_student(
           id,
           student.name,
           student.age, 
           student.email, 
                student.country, 
                student.id_number)
       return{"message": "Student Updated"}

@app.put("/teachers/{id}")
def update_teacher(id:int ,teacher:Teacher):
   update_teacher(
       id,
       teacher.name,
       teacher.age,
       teacher.email,
       teacher.department,
       teacher.employee_id
       
) 
   return{
    "message": "Teacher Updated"
}  

 
@app.put("/courses/{id}")
def update_course(id:int , course: Course):
       update_course(
            id,
           course.course_name,
           course.course_code,
           course.credits,
           course.year,
           course.trainer
       ) 
       return{"message": "Course updated"}




@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    delete_student(student_id)
    return {"message":f"Student with ID {student_id} deleted successfully"}

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    delete_teacher(teacher_id)
    return {"message": f"Teacher with ID {teacher_id} deleted successfully"}

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    delete_course(course_id)
    return {"message": f"Course with ID {course_id} deleted successfully"}