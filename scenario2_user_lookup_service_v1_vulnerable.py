"""
scenario2_user_lookup_service.py

Senaryo 2 - V1 ZAFİYETLİ HAL
İlk merge için kullanılır.
Beklenen: review failed + auto revert success
"""

import sqlite3
import hashlib
import random

DB_NAME = "scenario2_users.db"

# ZAFİYET-01: Hardcoded secret
APP_SECRET = "hardcoded-secret-123"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        )
    """)

    cursor.execute("DELETE FROM users")

    # ZAFİYET-02: Plain text password storage
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'admin123', 'admin')")
    cursor.execute("INSERT INTO users VALUES (2, 'kerem', '123456', 'user')")

    conn.commit()
    conn.close()


def login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ZAFİYET-03: SQL Injection
    query = f"SELECT id, username, role FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"success": False, "message": "Invalid credentials"}

    # ZAFİYET-04: Predictable token generation
    random.seed(username)

    # ZAFİYET-05: Weak hash algorithm
    token = hashlib.md5(f"{username}-{random.randint(1000, 9999)}-{APP_SECRET}".encode()).hexdigest()

    return {
        "success": True,
        "user": user,
        "token": token
    }


def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ZAFİYET-06: SQL Injection
    query = f"SELECT id, username, password, role FROM users WHERE id={user_id}"
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()

    # ZAFİYET-07: Sensitive data exposure
    return user


def main():
    init_db()

    print("Vulnerable user lookup service started.")

    result = login("admin", "admin123")
    print("Login result:", result)

    user = get_user("1")
    print("User detail:", user)


if __name__ == "__main__":
    main()