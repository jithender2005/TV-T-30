import sqlite3
from datetime import datetime

DB_PATH = "attendance.db"

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT,
            name TEXT,
            roll TEXT,
            date TEXT,
            time TEXT
        )
    """)

    # Admins table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    # Insert default admin if not exists
    cursor.execute("SELECT * FROM admins WHERE username = ?", ('admin',))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ('admin', 'admin123'))
        cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ('prathik', 'admin123'))
        cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ('jithender', 'admin123'))
    conn.commit()
    conn.close()

def log_attendance(uid, name, roll):
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM attendance WHERE name = ? AND date = ?
    """, (name, date))

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO attendance (uid, name, roll, date, time)
            VALUES (?, ?, ?, ?, ?)
        """, (uid, name, roll, date, time))
        conn.commit()

    conn.close()

def get_today_attendance():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT name, roll, time, date FROM attendance WHERE date = ?", (today,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"Name": row[0], "Roll": row[1], "Time": row[2], "Date": row[3]}
        for row in rows
    ]

def get_all_attendance():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, roll, time, date FROM attendance")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"Name": row[0], "Roll": row[1], "Time": row[2], "Date": row[3]}
        for row in rows
    ]

def validate_admin(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
    admin = cursor.fetchone()
    conn.close()
    return admin is not None
