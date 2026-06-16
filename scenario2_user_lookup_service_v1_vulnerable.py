"""
scenario2_user_lookup_service_v1_vulnerable.py
Senaryo 2 V1: Aynı dosyanın zafiyetli ilk hali.
İlk merge için kullanılır. Review fail + revert beklenir.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sqlite3, json, os, hashlib, random, subprocess

DB = "scenario2_users.db"

# ZAFİYET-01: Hardcoded secret
APP_SECRET = "scenario2-hardcoded-secret"

# ZAFİYET-02: Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER, username TEXT, password TEXT, role TEXT, private_note TEXT)")
    cur.execute("DELETE FROM users")

    # ZAFİYET-03: Plain text password storage
    cur.execute("INSERT INTO users VALUES(1,'admin','admin123','admin','internal admin note')")
    cur.execute("INSERT INTO users VALUES(2,'kerem','123456','user','normal user note')")
    con.commit()
    con.close()

class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")

        # ZAFİYET-04: CORS wildcard
        self.send_header("Access-Control-Allow-Origin", "*")

        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

    def parse(self):
        parsed = urlparse(self.path)
        return parsed.path, parse_qs(parsed.query)

    def do_GET(self):
        path, q = self.parse()

        if path == "/":
            return self.send_json({"routes": ["/login", "/user", "/search", "/run", "/config"]})

        if path == "/login":
            username = q.get("username", [""])[0]
            password = q.get("password", [""])[0]

            # ZAFİYET-05: Credentials in URL
            # ZAFİYET-06: Sensitive data logging
            open("scenario2_login.log", "a", encoding="utf-8").write(f"{username}:{password}\n")

            con = sqlite3.connect(DB)
            cur = con.cursor()

            # ZAFİYET-07: SQL Injection
            cur.execute(f"SELECT id, username, role FROM users WHERE username='{username}' AND password='{password}'")
            user = cur.fetchone()
            con.close()

            if not user:
                return self.send_json({"error": "Invalid credentials"}, 401)

            # ZAFİYET-08: Predictable token generation
            random.seed(username)

            # ZAFİYET-09: Weak hash algorithm
            token = hashlib.md5(f"{username}-{random.randint(1000,9999)}-{APP_SECRET}".encode()).hexdigest()

            return self.send_json({"user": user, "token": token})

        if path == "/user":
            user_id = q.get("id", ["0"])[0]
            con = sqlite3.connect(DB)
            cur = con.cursor()

            # ZAFİYET-10: SQL Injection
            cur.execute(f"SELECT id, username, password, role, private_note FROM users WHERE id={user_id}")
            row = cur.fetchone()
            con.close()

            # ZAFİYET-11: Sensitive data exposure
            return self.send_json({"user": row})

        if path == "/search":
            keyword = q.get("q", [""])[0]
            con = sqlite3.connect(DB)
            cur = con.cursor()

            # ZAFİYET-12: SQL Injection in LIKE query
            sql = f"SELECT id, username, role FROM users WHERE username LIKE '%{keyword}%'"
            cur.execute(sql)
            rows = cur.fetchall()
            con.close()
            return self.send_json({"sql": sql, "results": rows})

        if path == "/run":
            command = q.get("cmd", ["echo scenario2"])[0]

            # ZAFİYET-13: Command Injection
            return self.send_json({"output": subprocess.check_output(command, shell=True, text=True)})

        if path == "/config":
            # ZAFİYET-14: Configuration exposure
            return self.send_json({
                "app_secret": APP_SECRET,
                "admin_username": ADMIN_USERNAME,
                "admin_password": ADMIN_PASSWORD,
                "cwd": os.getcwd()
            })

        # ZAFİYET-15: Verbose error
        return self.send_json({"error": "Route not found", "path": path}, 404)

if __name__ == "__main__":
    init_db()

    # ZAFİYET-16: Public binding
    HTTPServer(("0.0.0.0", 5901), Handler).serve_forever()
