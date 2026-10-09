import sqlite3
from faker import Faker
from random import randint

fake = Faker()
DB_FILE = "data.db"
SUBJECTS = ["Math", "Science", "History", "Art", "Music"]
TEACHERS = [fake.name() for _ in range(8)]  # Generate 5 random teacher names
STUDENTS = [fake.name() for _ in range(50)]  # Generate 50 random student names
GROUPS = ["Alpha", "Beta", "Gamma"]  # Example group names


class Database:
    def __init__(self, db_file):
        # 1. Establish connection
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_tables()
        
    def execute_query(self, query, params=()):
        """
        Executes a query (INSERT, UPDATE, DELETE, CREATE TABLE)
        and commits the changes.
        Returns the number of affected rows.
        """
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"Database error during execution: {e}{params}")
            self.connection.rollback() # Rollback if anything failed
            return 0

    def fetch_data(self, query, params=()):
        """
        Executes a SELECT query and returns all fetched results.
        """
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error during fetching: {e}")
            return None

    def create_tables(self):
        """Creates the necessary tables if they don't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                "id"	INTEGER NOT NULL,
                "group_name"	VARCHAR(10) NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                "id"	INTEGER NOT NULL,
                "subject_name"	VARCHAR(10) NOT NULL,
                "teacher_id" INTEGER NOT NULL,
                FOREIGN KEY (teacher_id) REFERENCES teachers (id)
                PRIMARY KEY("id" AUTOINCREMENT)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                "id"	INTEGER NOT NULL,
                "teacher_name"	VARCHAR(50) NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
            "id" INTEGER NOT NULL,
            "name" VARCHAR(30), 
            "group_id" INT,
            PRIMARY KEY("id" AUTOINCREMENT)
            FOREIGN KEY (group_id)
            REFERENCES groups (id)
              
            )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks(
        "id" INTEGER NOT NULL,
        "score" INT NOT NULL,
        "subject_id" INT NOT NULL,
        "student_id" INT NOT NULL,
        "date" DATE DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY("id" AUTOINCREMENT)
        FOREIGN KEY (subject_id) REFERENCES subjects (id) 
        ON DELETE SET NULL
        ON UPDATE CASCADE,
        FOREIGN KEY (student_id) REFERENCES students (id)
        
        )
        """)

        self.connection.commit()

    def close(self):
        """Closes the database connection."""
        self.connection.close()
        print("Database connection closed.")


db = None # Initialize db outside try block for scope

try:
    # 1. Initialize Database connection and tables
    db = Database(DB_FILE)
   
    for i, group in enumerate(GROUPS, start=1):
        insert_group_query = "INSERT INTO groups (id, group_name) VALUES (?, ?)"
        db.execute_query(insert_group_query, (i, group))
    for i, subject in enumerate(SUBJECTS, start=1):
        insert_subject_query = "INSERT INTO subjects (id, subject_name, teacher_id) VALUES (?, ?, ?)"
        db.execute_query(insert_subject_query, (i, subject, randint(1, 8)))  # Assuming teacher_id is same as id for simplicity
    for i, teacher in enumerate(TEACHERS, start=1):
        insert_teacher_query = "INSERT INTO teachers (id, teacher_name) VALUES (?, ?)"
        db.execute_query(insert_teacher_query, (i, teacher))
    for i, student in enumerate(STUDENTS, start=1):
        insert_student_query = "INSERT INTO students (id, name, group_id) VALUES (?, ?, ?)"
        db.execute_query(insert_student_query, (i, student, randint(1, 3)))  # Randomly assign group_id between 1 and 3
    for i in range(1, 11):
        for s,student in enumerate(STUDENTS, start=1):
            for j,subject in enumerate(SUBJECTS, start=1):
                insert_mark_query = "INSERT INTO marks (score, subject_id, student_id) VALUES (?, ?, ?)"
                db.execute_query(insert_mark_query, (randint(1, 12), j, STUDENTS.index(student) + 1))
    
    print("Data inserted successfully.")

except sqlite3.Error as e:
    print(f"\n[CRITICAL ERROR]: A database error occurred: {e}")

finally:
    if db:
        db.close()
