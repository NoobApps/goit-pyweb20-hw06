import sqlite3
from faker import Faker
from random import randint

fake = Faker()
DB_FILE = "data.db"
SUBJECTS = ["Math", "Science", "History", "Art", "Music", "Chemistry", "Geography"]
TEACHERS = [fake.name() for _ in range(5)]  # Generate 5 random teacher names
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
   
    for group in GROUPS:
        insert_group_query = "INSERT INTO groups (group_name) VALUES (?)"
        db.execute_query(insert_group_query, (group,))
    for subject in SUBJECTS:
        insert_subject_query = "INSERT INTO subjects (subject_name, teacher_id) VALUES (?, ?)"
        db.execute_query(insert_subject_query, (subject, randint(1, len(TEACHERS))))  # Assuming teacher_id is same as id for simplicity
    for teacher in TEACHERS:
        insert_teacher_query = "INSERT INTO teachers (teacher_name) VALUES (?)"
        db.execute_query(insert_teacher_query, (teacher,))
    for student in STUDENTS:
        insert_student_query = "INSERT INTO students (name, group_id) VALUES (?, ?)"
        db.execute_query(insert_student_query, (student, randint(1, len(GROUPS))))  # Randomly assign group_id between 1 and 3
    for i in range(1, 11):
        for student in STUDENTS:
            for subject in SUBJECTS:
                insert_mark_query = "INSERT INTO marks (score, subject_id, student_id, date) VALUES (?, ?, ?, ?)"
                db.execute_query(insert_mark_query, (randint(1, 12), SUBJECTS.index(subject)+1, STUDENTS.index(student) + 1,fake.date_this_year()))
    
    print("Data inserted successfully.")

except sqlite3.Error as e:
    print(f"\n[CRITICAL ERROR]: A database error occurred: {e}")

finally:
    if db:
        db.close()
