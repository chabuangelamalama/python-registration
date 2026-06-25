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
                           SET name = ?, age = ?, email= ? country=?, id_number= ?
                           WHERE id = ? 
                           """(name, age, email, department, employee_id))
    
