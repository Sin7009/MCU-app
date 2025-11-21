import sqlite3
from typing import List, Optional, Tuple

DB_NAME = "schedule_mgpu.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    """Initialize the database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create Teachers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT,
            preferences TEXT  -- Text field to store things like "No Mondays", etc.
        )
    ''')

    # Create Disciplines table (represents the Study Plan items)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disciplines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL,
            hours INTEGER,
            group_name TEXT,
            semester INTEGER,
            teacher_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    ''')

    conn.commit()
    conn.close()

# --- Teacher Operations ---

def add_teacher(full_name: str, email: str, preferences: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO teachers (full_name, email, preferences) VALUES (?, ?, ?)',
                   (full_name, email, preferences))
    conn.commit()
    conn.close()

def get_all_teachers() -> List[Tuple]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM teachers')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_teacher_by_id(teacher_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM teachers WHERE id = ?', (teacher_id,))
    row = cursor.fetchone()
    conn.close()
    return row

# --- Discipline Operations ---

def add_discipline(subject_name: str, hours: int, group_name: str, semester: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO disciplines (subject_name, hours, group_name, semester)
        VALUES (?, ?, ?, ?)
    ''', (subject_name, hours, group_name, semester))
    conn.commit()
    conn.close()

def get_all_disciplines() -> List[Tuple]:
    conn = get_connection()
    cursor = conn.cursor()
    # Join with teachers to get the teacher name if assigned
    cursor.execute('''
        SELECT d.id, d.subject_name, d.hours, d.group_name, d.semester, t.full_name
        FROM disciplines d
        LEFT JOIN teachers t ON d.teacher_id = t.id
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def assign_teacher_to_discipline(discipline_id: int, teacher_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE disciplines SET teacher_id = ? WHERE id = ?', (teacher_id, discipline_id))
    conn.commit()
    conn.close()

def clear_disciplines():
    """Clears all disciplines (useful when reloading a plan)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM disciplines')
    conn.commit()
    conn.close()
