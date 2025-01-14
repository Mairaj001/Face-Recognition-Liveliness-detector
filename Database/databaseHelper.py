import sqlite3

DB_PATH = "Database/user.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(open("database/schema.sql").read())
    conn.commit()
    conn.close()

def register_user(name, email, image_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, image_path) VALUES (?, ?, ?)", (name, email, image_path))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("User with this email already exists.")
    finally:
        conn.close()

def get_user_by_name(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    conn.close()
    return user
