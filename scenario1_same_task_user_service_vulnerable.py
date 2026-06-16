"""
scenario1_same_task_user_service_vulnerable.py

Senaryo 1: Aynı task düzeltme testi - İLK MERGE için zafiyetli dosya.
Amaç:
    1) Bu dosyayı source task branch'e ekle.
    2) Merge et.
    3) Review fail olsun.
    4) Auto-revert çalışsın.
    5) dev_mergeable=false olsun.

Gerçek ortamda kullanmayın.
Çalıştırma:
    python scenario1_same_task_user_service_vulnerable.py
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sqlite3
import json
import hashlib
import random
import subprocess
import os

DB_NAME = "scenario1_users.db"

# ZAFİYET-01: Hardcoded secret
APP_SECRET = "scenario1-hardcoded-secret"

# ZAFİYET-02: Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, private_note TEXT)"
    )

    cur.execute("DELETE FROM users")

    # ZAFİYET-03: Plain text password storage
    cur.execute("INSERT INTO users VALUES (1, 'admin', 'admin123', 'admin', 'internal admin note')")
    cur.execute("INSERT INTO users VALUES (2, 'kerem', '123456', 'user', 'normal user note')")

    conn.commit()
    conn.close()


class VulnerableUserService(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")

        # ZAFİYET-04: CORS wildcard
        self.send_header("Access-Control-Allow-Origin", "*")

        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

    def parse_request(self):
        parsed = urlparse(self.path)
        return parsed.path, parse_qs(parsed.query)

    def do_GET(self):
        path, query = self.parse_request()

        if path == "/":
            return self.send_json({
                "message": "Scenario 1 vulnerable user service",
                "routes": ["/login", "/user", "/search", "/run", "/config"]
            })

        if path == "/login":
            username = query.get("username", [""])[0]
            password = query.get("password", [""])[0]

            # ZAFİYET-05: Credentials in URL
            # ZAFİYET-06: Sensitive data logging
            with open("scenario1_login.log", "a", encoding="utf-8") as log_file:
                log_file.write(f"username={username}, password={password}\n")

            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()

            # ZAFİYET-07: SQL Injection
            sql = f"SELECT id, username, role FROM users WHERE username='{username}' AND password='{password}'"
            cur.execute(sql)
            user = cur.fetchone()
            conn.close()

            if not user:
                return self.send_json({"error": "Invalid credentials"}, 401)

            # ZAFİYET-08: Predictable token generation
            random.seed(username)

            # ZAFİYET-09: Weak hash algorithm
            token = hashlib.md5(f"{username}-{random.randint(1000,9999)}-{APP_SECRET}".encode()).hexdigest()

            return self.send_json({"status": "success", "user": user, "token": token})

        if path == "/user":
            user_id = query.get("id", ["0"])[0]

            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()

            # ZAFİYET-10: SQL Injection
            cur.execute(f"SELECT id, username, password, role, private_note FROM users WHERE id={user_id}")
            row = cur.fetchone()
            conn.close()

            # ZAFİYET-11: Sensitive data exposure
            return self.send_json({"user": row})

        if path == "/search":
            keyword = query.get("q", [""])[0]

            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()

            # ZAFİYET-12: SQL Injection in LIKE query
            sql = f"SELECT id, username, role FROM users WHERE username LIKE '%{keyword}%'"
            cur.execute(sql)
            rows = cur.fetchall()
            conn.close()

            return self.send_json({"sql": sql, "results": rows})

        if path == "/run":
            command = query.get("cmd", ["echo scenario1"])[0]

            # ZAFİYET-13: Command Injection
            output = subprocess.check_output(command, shell=True, text=True)
            return self.send_json({"command": command, "output": output})

        if path == "/config":
            # ZAFİYET-14: Configuration exposure
            return self.send_json({
                "app_secret": APP_SECRET,
                "admin_username": ADMIN_USERNAME,
                "admin_password": ADMIN_PASSWORD,
                "db_name": DB_NAME,
                "cwd": os.getcwd()
            })

        # ZAFİYET-15: Verbose error
        return self.send_json({"error": "Route not found", "path": path}, 404)


if __name__ == "__main__":
    init_db()

    # ZAFİYET-16: Public binding
    HTTPServer(("0.0.0.0", 6001), VulnerableUserService).serve_forever()
