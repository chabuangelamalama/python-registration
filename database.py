import sqlite3
from contextlib import contextmanager

sqlite_file_name ="school.db"
@contextmanager
def get_connection():
    connection = sqlite3.connect(sqlite_file_name)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()

    finally:
        connection.close()

###STUDENTS 
def create_table():
    with get_connection() as connection:
        connection.execute( ''' CREATE TABLE IF NOT EXISTS students (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          age INTEGER NOT NULL,
                          email TEXT NOT NULL, 
                          country TEXT NOT NULL,
                          id_number INTEGER NOT NULL)''')



        connection.execute('''CREATE TABLE IF NOT EXISTS teachers (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          email TEXT NOT NULL UNIQUE,
                          department TEXT NOT NULL,
                          employee_id TEXT NOT NULL,
                          age INTEGER NOT NULL)''')
        
        connection.execute('''CREATE TABLE IF NOT EXISTS courses (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          course_code TEXT NOT NULL UNIQUE,
                          course_name 
                          credits TEXT NOT NULL,
                          description TEXT NOT NULL,
                          trainer TEXT NOT NULL)''')
          

        

        

def add_student(name, age, email,country, id_number):
    with get_connection() as connection:
        connection.execute(
            'INSERT INTO students (name, age, email, country, id_number) VALUES (?, ?, ?, ?, ?)', 
             (name, age, email, country, id_number),
        )

def add_teacher(name, age, email, department, employee_id):
    with get_connection() as connection:
        connection.execute(
            'INSERT INTO teachers (name, age, email, department, employee_id) VALUES (?, ?, ?, ?, ?)', 
             (name, age, email, department, employee_id),
        )


def add_course(course_name, course_code,credits, year, trainer):
    with get_connection() as connection:
        connection.execute(
            'INSERT INTO courses (course_name,course_code,credits.year,trainer) VALUES (?, ?, ?, ?, ?)', 
             (course_name, course_code, credits, year, trainer),
        )

def get_students():
    with get_connection() as connection:
        return connection.execute('SELECT * FROM students').fetchall()

def get_teachers():
    with get_connection() as connection:
        return connection.execute('SELECT * FROM teachers').fetchall()


def get_courses():
    with get_connection() as connection:
        return connection.execute('SELECT * FROM courses').fetchall()
    

def update_students(id,name, age, email, country, id_number):
    with get_connection() as connection:
        connection.execute(""" UPDATE students 
                           SET name = ?, age = ?, email= ? country=?, id_number= ?
                           WHERE id = ? 
                           """(name, age, email, country, id_number))
        


def update_teachers(name, age, email, department, employee_id):
    with get_connection() as connection:
        connection.execute(""" UPDATE teachers
                           SET name = ?, age = ?, email= ? department=?, employee_id= ?
                           WHERE id = ? 
                           """(name, age, email, department, employee_id))
    

def update_courses(course_name, course_code, credits, year, trainer):
    with get_connection() as connection:
        connection.execute(""" UPDATE courses
                           SET course_name = ?, course_code = ?, credits= ? year=?,  trainer= ?
                           WHERE id = ? 
                           """(course_name, course_code, credits, year, trainer))
        

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


def update_student(student_id, name, age, email, country, id_number):
    with get_connection() as connection:
        connection.execute(
            '''UPDATE students SET name = ?, age = ?, email = ?, country = ?, id_number = ?
            WHERE id = ?''',
            (name, age, email,country, id_number, student_id,)
        )

def update_teacher(teacher_id, name, age, email, department, employee_id):
    with get_connection() as connection:
        connection.execute(
            '''UPDATE teachers
            SET name=?, age=?, email=?, department=?, employee_id=?
            WHERE id=?''',
            (name, age, email, department, employee_id, teacher_id)
        )

def update_course(course_id, course_name, course_code, credits, year, trainer):
    with get_connection() as connection:
        connection.execute(
            '''UPDATE courses
            SET course_name=?, course_code=?, credits=?, year=?, trainer=?
            WHERE id=?''',
            (course_name, course_code, credits, year, trainer, course_id)
        )


def delete_student(student_id):
    with get_connection() as connection:
        connection.execute(
            'DELETE FROM students WHERE id = ?',
            (student_id)
        )


def delete_teacher(teacher_id):
    with get_connection() as connection:
        connection.execute(
            'DELETE FROM teachers WHERE id=?',
            (teacher_id,)
        )

def delete_course(course_id):
    with get_connection() as connection:
        connection.execute(
            'DELETE FROM courses WHERE id=?',
            (course_id,)
        )