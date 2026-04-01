import sqlite3
import bcrypt

# Create database and users table
def create_users_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()


# Register user
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hashed_pw))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


# Login user
def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    data = c.fetchone()

    conn.close()

    if data:
        stored_pw = data[0]
        if bcrypt.checkpw(password.encode(), stored_pw):
            return True

    return False