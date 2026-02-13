import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            age INTEGER,
            gender TEXT,
            tumor TEXT,
            confidence REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_record(name, age, gender, tumor, confidence):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO records (patient_name, age, gender, tumor, confidence)
        VALUES (?, ?, ?, ?, ?)
    """, (name, age, gender, tumor, confidence))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM records ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()
    return data


def get_dashboard_data():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT tumor, gender FROM records")
    data = cursor.fetchall()

    conn.close()
    return data
