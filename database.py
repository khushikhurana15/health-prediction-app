import sqlite3

DB_NAME = "patients.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                dob TEXT NOT NULL,
                email TEXT NOT NULL,
                glucose REAL NOT NULL,
                haemoglobin REAL NOT NULL,
                cholesterol REAL NOT NULL,
                remarks TEXT
            )
        """)
        conn.commit()

def create_patient(name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patients (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks))
        conn.commit()

def read_all_patients():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        return cursor.fetchall()

def update_patient(patient_id, name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE patients 
            SET full_name=?, dob=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, remarks=?
            WHERE id=?
        """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks, patient_id))
        conn.commit()

def delete_patient(patient_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
        conn.commit()
    check_and_vacuum_if_empty()

def check_and_vacuum_if_empty():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM patients")
        count = cursor.fetchone()[0]
        
    if count == 0:
        conn = sqlite3.connect(DB_NAME)
        conn.isolation_level = None  
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='patients'")
        except sqlite3.OperationalError:
            pass 
        
        cursor.execute("VACUUM") 
        conn.close()

def reset_database_completely():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS patients")
        conn.commit()
    init_db()
