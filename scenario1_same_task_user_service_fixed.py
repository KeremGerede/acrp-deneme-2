"""
scenario1_same_task_user_service_fixed.py

Senaryo 1: Aynı task düzeltme testi - İKİNCİ MERGE için düzeltilmiş temiz dosya.
Amaç:
    1) İlk zafiyetli merge fail/revert olduktan sonra aynı task branch'e geç.
    2) Zafiyetli dosyanın içeriğini bu temiz versiyonla değiştir.
    3) Tekrar commit/push ve merge et.
    4) Review success beklenir.
    5) dev_mergeable=true ve last_block_reason=null beklenir.

Çalıştırma:
    python scenario1_same_task_user_service_fixed.py
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import secrets
import sqlite3
from http import HTTPStatus

DB_NAME = "scenario1_users_fixed.db"


def init_db() -> None:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, role TEXT)"
    )

    cur.execute("DELETE FROM users")

    users = [
        (1, "admin", "admin-demo-password-hash", "admin"),
        (2, "kerem", "user-demo-password-hash", "user"),
    ]

    cur.executemany(
        "INSERT INTO users (id, username, password_hash, role) VALUES (?, ?, ?, ?)",
        users,
    )

    conn.commit()
    conn.close()


def find_user(username: str) -> tuple[int, str, str] | None:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, role FROM users WHERE username = ?",
        (username,),
    )

    row = cur.fetchone()
    conn.close()
    return row


def get_user_by_id(user_id: int) -> tuple[int, str, str] | None:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, role FROM users WHERE id = ?",
        (user_id,),
    )

    row = cur.fetchone()
    conn.close()
    return row


def search_users(keyword: str) -> list[tuple[int, str, str]]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, role FROM users WHERE username LIKE ?",
        (f"%{keyword}%",),
    )

    rows = cur.fetchall()
    conn.close()
    return rows


class CleanUserService(BaseHTTPRequestHandler):
    def send_json(self, data: dict, status: int = HTTPStatus.OK) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

    def parse_request(self):
        parsed = urlparse(self.path)
        return parsed.path, parse_qs(parsed.query)

    def do_GET(self):
        path, query = self.parse_request()

        if path == "/":
            return self.send_json({
                "message": "Scenario 1 fixed user service",
                "routes": ["/login", "/user", "/search"]
            })

        if path == "/login":
            username = query.get("username", [""])[0].strip()

            if not username:
                return self.send_json({"error": "username is required"}, HTTPStatus.BAD_REQUEST)

            user = find_user(username)

            if not user:
                return self.send_json({"error": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED)

            token = secrets.token_urlsafe(32)

            return self.send_json({
                "status": "success",
                "user": {
                    "id": user[0],
                    "username": user[1],
                    "role": user[2],
                },
                "token": token,
            })

        if path == "/user":
            raw_user_id = query.get("id", [""])[0]

            try:
                user_id = int(raw_user_id)
            except ValueError:
                return self.send_json({"error": "id must be an integer"}, HTTPStatus.BAD_REQUEST)

            user = get_user_by_id(user_id)

            if not user:
                return self.send_json({"error": "User not found"}, HTTPStatus.NOT_FOUND)

            return self.send_json({
                "user": {
                    "id": user[0],
                    "username": user[1],
                    "role": user[2],
                }
            })

        if path == "/search":
            keyword = query.get("q", [""])[0].strip()

            if len(keyword) > 50:
                return self.send_json({"error": "search keyword is too long"}, HTTPStatus.BAD_REQUEST)

            rows = search_users(keyword)

            return self.send_json({
                "results": [
                    {"id": row[0], "username": row[1], "role": row[2]}
                    for row in rows
                ]
            })

        return self.send_json({"error": "Route not found"}, HTTPStatus.NOT_FOUND)


if __name__ == "__main__":
    init_db()
    HTTPServer(("127.0.0.1", 6001), CleanUserService).serve_forever()
