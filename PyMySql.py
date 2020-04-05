import mysql.connector


def test_connection():
    db_connection = get_db_connection()
    print(db_connection)


def create_my_first_db():
    db_connection = get_db_connection()
    # creating database_cursor to perform SQL operation
    db_cursor = db_connection.cursor()
    # executing cursor with execute method and pass SQL query
    db_cursor.execute("CREATE DATABASE my_first_db")
    # get list of all databases
    db_cursor.execute("SHOW DATABASES")
    # print all databases
    for db in db_cursor:
        print(db)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="flea_bag"
    )


def create_student_table():
    db_connection = get_db_connection()
    db_connection.database = "my_first_db"
    db_cursor = db_connection.cursor()
    # Here creating database table as student'
    db_cursor.execute("CREATE TABLE student (id INT, name VARCHAR(255))")
    # Get database table'
    db_cursor.execute("SHOW TABLES")
    for table in db_cursor:
        print(table)


def create_employee_table():
    db_connection = get_db_connection()
    db_connection.database = "my_first_db"
    db_cursor = db_connection.cursor()
    #Here creating database table as employee with primary key
    db_cursor.execute("CREATE TABLE employee(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), salary INT(6))")
    #Get database table
    db_cursor.execute("SHOW TABLES")
    for table in db_cursor:
        print(table)


def alter_student_table():
    db_connection = get_db_connection()
    db_connection.database = "my_first_db"
    db_cursor = db_connection.cursor()
    # Here we modify existing column id
    db_cursor.execute("ALTER TABLE student MODIFY id INT PRIMARY KEY")


def insert_student_employee():
    db_connection = get_db_connection()
    db_connection.database = "my_first_db"
    db_cursor = db_connection.cursor()
    student_sql_query = "INSERT INTO student(id,name) VALUES(01, 'John')"
    employee_sql_query = " INSERT INTO employee (id, name, salary) VALUES (01, 'John', 10000)"
    # Execute cursor and pass query as well as student data
    db_cursor.execute(student_sql_query)
    # Execute cursor and pass query of employee and data of employee
    db_cursor.execute(employee_sql_query)
    db_connection.commit()
    print(db_cursor.rowcount, "Record Inserted")


create_my_first_db()


