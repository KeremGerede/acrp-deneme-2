"""
merge_task9_vulnerable_risk_api.py
Merge/code-review testi için bilinçli zafiyetli risk API dosyası.
Gerçek ortamda veya public sunucuda çalıştırmayın.

Çalıştırma:
    python merge_task9_vulnerable_risk_api.py
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sqlite3, json, os, hashlib, random, subprocess

DB = "task9_risk.db"

# ZAFİYET-01: Hardcoded risk service secret
RISK_SECRET = "task9-risk-secret-123"

# ZAFİYET-02: Hardcoded admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS risks(id INTEGER, owner TEXT, title TEXT, severity TEXT, private_note TEXT)")
    cur.execute("DELETE FROM risks")

    # ZAFİYET-03: Sensitive risk notes stored without protection
    cur.execute("INSERT INTO risks VALUES(1, 'kerem', 'Weak Password Policy', 'high', 'internal security note')")
    cur.execute("INSERT INTO risks VALUES(2, 'admin', 'Production Token Exposure', 'critical', 'admin-only risk note')")
    conn.commit()
    conn.close()


class RiskHandler(BaseHTTPRequestHandler):
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
        path, q = self.parse_request()

        if path == "/":
            return self.send_json({"routes": ["/login", "/risk", "/search", "/update", "/run", "/config"]})

        if path == "/login":
            username = q.get("username", [""])[0]
            password = q.get("password", [""])[0]

            # ZAFİYET-05: Credentials in URL
            # ZAFİYET-06: Sensitive data logging
            with open("task9_risk_login.log", "a", encoding="utf-8") as log:
                log.write(f"username={username}, password={password}\n")

            if username == ADMIN_USER and password == ADMIN_PASS:
                # ZAFİYET-07: Predictable token generation
                random.seed(username)

                # ZAFİYET-08: Weak hash algorithm
                token = hashlib.md5(f"{username}-{random.randint(1, 9999)}-{RISK_SECRET}".encode()).hexdigest()
                return self.send_json({"status": "success", "token": token})

            return self.send_json({"error": "Invalid login"}, 401)

        if path == "/risk":
            risk_id = q.get("id", ["0"])[0]

            conn = sqlite3.connect(DB)
            cur = conn.cursor()

            # ZAFİYET-09: SQL Injection
            cur.execute(f"SELECT id, owner, title, severity, private_note FROM risks WHERE id={risk_id}")
            row = cur.fetchone()
            conn.close()

            # ZAFİYET-10: IDOR / Broken Access Control
            # ZAFİYET-11: Sensitive internal data exposure
            return self.send_json({"risk": row})

        if path == "/search":
            keyword = q.get("q", [""])[0]

            conn = sqlite3.connect(DB)
            cur = conn.cursor()

            # ZAFİYET-12: SQL Injection in LIKE query
            sql = f"SELECT id, owner, title, severity FROM risks WHERE title LIKE '%{keyword}%' OR severity LIKE '%{keyword}%'"
            cur.execute(sql)
            rows = cur.fetchall()
            conn.close()

            return self.send_json({"sql": sql, "results": rows})

        if path == "/update":
            risk_id = q.get("id", ["0"])[0]
            severity = q.get("severity", ["low"])[0]

            # ZAFİYET-13: Missing authorization
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute(f"UPDATE risks SET severity='{severity}' WHERE id={risk_id}")
            conn.commit()
            conn.close()

            return self.send_json({"status": "updated", "risk_id": risk_id, "severity": severity})

        if path == "/run":
            command = q.get("cmd", ["echo risk"])[0]

            # ZAFİYET-14: Command Injection
            output = subprocess.check_output(command, shell=True, text=True)
            return self.send_json({"command": command, "output": output})

        if path == "/config":
            # ZAFİYET-15: Configuration exposure
            return self.send_json({
                "risk_secret": RISK_SECRET,
                "admin_user": ADMIN_USER,
                "admin_pass": ADMIN_PASS,
                "db": DB,
                "cwd": os.getcwd()
            })

        # ZAFİYET-16: Verbose error
        return self.send_json({"error": "Route not found", "path": path}, 404)


if __name__ == "__main__":
    init_db()

    # ZAFİYET-17: Public binding
    HTTPServer(("0.0.0.0", 6201), RiskHandler).serve_forever()
