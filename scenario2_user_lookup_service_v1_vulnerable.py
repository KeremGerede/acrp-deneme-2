"""
scenario2_user_lookup_service.py

Senaryo 2 - V2 DÜZELTİLMİŞ HAL
Aynı dosyada zafiyetli satırlar temizlendi.
Beklenen: review success + dev_mergeable=true
"""

import sqlite3
import hashlib
import secrets

DB_NAME = "scenario2_users.db"


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT
        )
    """)

    cursor.execute("DELETE FROM users")

    users = [
        (1, "admin", hash_password("admin123"), "admin"),
        (2, "kerem", hash_password("123456"), "user"),
    ]

    cursor.executemany(
        "INSERT INTO users VALUES (?, ?, ?, ?)",
        users
    )

    conn.commit()
    conn.close()


def login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"success": False, "message": "Invalid credentials"}

    expected_password_hash = user[2]

    if hash_password(password) != expected_password_hash:
        return {"success": False, "message": "Invalid credentials"}

    token = secrets.token_urlsafe(32)

    return {
        "success": True,
        "user": {
            "id": user[0],
            "username": user[1],
            "role": user[3]
        },
        "token": token
    }


def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, role FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return None

    return {
        "id": user[0],
        "username": user[1],
        "role": user[2]
    }


def main():
    init_db()

    print("Fixed user lookup service started.")

    result = login("admin", "admin123")
    print("Login result:", result)

    user = get_user(1)
    print("User detail:", user)


if __name__ == "__main__":
    main()