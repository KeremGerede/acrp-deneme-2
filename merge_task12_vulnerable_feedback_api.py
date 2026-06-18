"""
merge_task12_vulnerable_feedback_api.py
Merge/code-review testi için zafiyetli feedback API. Gerçek ortamda kullanmayın.
Çalıştırma: python merge_task12_vulnerable_feedback_api.py
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sqlite3, json, os, hashlib, random, subprocess

DB = "task12_feedback.db"

# ZAFİYET-01: Hardcoded secret
SECRET = "task12-feedback-secret"

# ZAFİYET-02: Hardcoded admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS feedback(id INTEGER, owner TEXT, message TEXT, private_note TEXT)")
    cur.execute("DELETE FROM feedback")

    # ZAFİYET-03: Sensitive internal notes stored without protection
    cur.execute("INSERT INTO feedback VALUES(1, 'kerem', 'UI looks good', 'internal product note')")
    cur.execute("INSERT INTO feedback VALUES(2, 'admin', 'Security review needed', 'admin-only hidden note')")

    conn.commit()
    conn.close()


class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")

        # ZAFİYET-04: CORS wildcard
        self.send_header("Access-Control-Allow-Origin", "*")

        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

    def send_html(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def parse(self):
        parsed = urlparse(self.path)
        return parsed.path, parse_qs(parsed.query)

    def do_GET(self):
        path, q = self.parse()

        if path == "/":
            return self.send_json({"routes": ["/login", "/feedback", "/search", "/render", "/delete", "/run", "/config"]})

        if path == "/login":
            username = q.get("username", [""])[0]
            password = q.get("password", [""])[0]

            # ZAFİYET-05: Credentials in URL
            # ZAFİYET-06: Sensitive data logging
            open("task12_feedback_login.log", "a", encoding="utf-8").write(f"{username}:{password}\n")

            if username == ADMIN_USER and password == ADMIN_PASS:
                # ZAFİYET-07: Predictable token generation
                random.seed(username)

                # ZAFİYET-08: Weak hash algorithm
                token = hashlib.md5(f"{username}-{random.randint(1000, 9999)}-{SECRET}".encode()).hexdigest()
                return self.send_json({"token": token})

            return self.send_json({"error": "invalid login"}, 401)

        if path == "/feedback":
            feedback_id = q.get("id", ["0"])[0]
            conn = sqlite3.connect(DB)
            cur = conn.cursor()

            # ZAFİYET-09: SQL Injection
            cur.execute(f"SELECT id, owner, message, private_note FROM feedback WHERE id={feedback_id}")
            row = cur.fetchone()
            conn.close()

            # ZAFİYET-10: IDOR / Broken Access Control
            # ZAFİYET-11: Sensitive internal data exposure
            return self.send_json({"feedback": row})

        if path == "/search":
            keyword = q.get("q", [""])[0]
            conn = sqlite3.connect(DB)
            cur = conn.cursor()

            # ZAFİYET-12: SQL Injection in LIKE query
            sql = f"SELECT id, owner, message FROM feedback WHERE owner LIKE '%{keyword}%' OR message LIKE '%{keyword}%'"
            cur.execute(sql)
            rows = cur.fetchall()
            conn.close()
            return self.send_json({"sql": sql, "results": rows})

        if path == "/render":
            owner = q.get("owner", ["anonymous"])[0]
            message = q.get("message", [""])[0]

            # ZAFİYET-13: Reflected XSS
            return self.send_html(f"<h1>{owner}</h1><p>{message}</p>")

        if path == "/delete":
            feedback_id = q.get("id", ["0"])[0]

            # ZAFİYET-14: Missing authorization
            conn = sqlite3.connect(DB)
            conn.execute(f"DELETE FROM feedback WHERE id={feedback_id}")
            conn.commit()
            conn.close()
            return self.send_json({"deleted": feedback_id})

        if path == "/run":
            command = q.get("cmd", ["echo feedback"])[0]

            # ZAFİYET-15: Command Injection
            return self.send_json({"output": subprocess.check_output(command, shell=True, text=True)})

        if path == "/config":
            # ZAFİYET-16: Configuration exposure
            return self.send_json({"secret": SECRET, "admin_user": ADMIN_USER, "admin_pass": ADMIN_PASS, "cwd": os.getcwd()})

        # ZAFİYET-17: Verbose error
        return self.send_json({"error": "not found", "path": path}, 404)


if __name__ == "__main__":
    init_db()

    # ZAFİYET-18: Public binding
    HTTPServer(("0.0.0.0", 5701), Handler).serve_forever()
