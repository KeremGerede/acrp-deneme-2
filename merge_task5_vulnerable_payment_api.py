"""
merge_task5_vulnerable_payment_api.py

Merge/code-review testi için bilinçli zafiyetli payment API dosyası.
Gerçek ortamda veya public sunucuda çalıştırmayın.

Çalıştırma:
    python merge_task5_vulnerable_payment_api.py

Tarayıcı:
    http://localhost:6601
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sqlite3
import json
import os
import hashlib
import random
import subprocess

DB_NAME = "task5_payment_api.db"

# ZAFİYET-01: Hardcoded payment secret
PAYMENT_SECRET = "task5-payment-secret-123"

# ZAFİYET-02: Hardcoded admin credentials
ADMIN_EMAIL = "admin@payment.local"
ADMIN_PASSWORD = "admin123"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY,
            user_email TEXT,
            card_number TEXT,
            amount REAL,
            status TEXT,
            private_note TEXT
        )
    """)

    cur.execute("DELETE FROM payments")

    # ZAFİYET-03: Sensitive card data stored in plain text
    cur.execute("INSERT INTO payments VALUES (1, 'kerem@example.com', '4111111111111111', 250.0, 'paid', 'internal fraud note')")
    cur.execute("INSERT INTO payments VALUES (2, 'admin@example.com', '5555555555554444', 999.0, 'pending', 'admin-only payment note')")

    conn.commit()
    conn.close()


class PaymentHandler(BaseHTTPRequestHandler):
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
                "message": "Task 5 Vulnerable Payment API",
                "routes": ["/login", "/payment", "/search", "/refund", "/run", "/config"]
            })

        if path == "/login":
            email = query.get("email", [""])[0]
            password = query.get("password", [""])[0]

            # ZAFİYET-05: Credentials in URL
            # ZAFİYET-06: Sensitive data logging
            with open("task5_payment_login.log", "a", encoding="utf-8") as log_file:
                log_file.write(f"email={email}, password={password}\n")

            if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                # ZAFİYET-07: Predictable token generation
                random.seed(email)

                # ZAFİYET-08: Weak hash algorithm
                token = hashlib.md5(f"{email}-{random.randint(1000,9999)}-{PAYMENT_SECRET}".encode()).hexdigest()
                return self.send_json({"status": "success", "token": token})

            return self.send_json({"error": "Invalid credentials"}, 401)

        if path == "/payment":
            payment_id = query.get("id", ["0"])[0]

            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()

            # ZAFİYET-09: SQL Injection
            cur.execute(f"SELECT id, user_email, card_number, amount, status, private_note FROM payments WHERE id={payment_id}")
            row = cur.fetchone()
            conn.close()

            if not row:
                return self.send_json({"error": "Payment not found"}, 404)

            # ZAFİYET-10: IDOR / Broken Access Control
            # ZAFİYET-11: Sensitive payment data exposure
            return self.send_json({
                "id": row[0],
                "user_email": row[1],
                "card_number": row[2],
                "amount": row[3],
                "status": row[4],
                "private_note": row[5]
            })

        if path == "/search":
            keyword = query.get("q", [""])[0]

            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()

            # ZAFİYET-12: SQL Injection in LIKE query
            sql = f"SELECT id, user_email, amount, status FROM payments WHERE user_email LIKE '%{keyword}%'"
            cur.execute(sql)
            rows = cur.fetchall()
            conn.close()

            return self.send_json({"sql": sql, "results": rows})

        if path == "/refund":
            payment_id = query.get("id", ["0"])[0]
            amount = float(query.get("amount", ["0"])[0])

            # ZAFİYET-13: Business logic flaw
            # Kullanıcı iade miktarını kendisi belirliyor, negatif/yüksek tutar kontrolü yok.

            # ZAFİYET-14: Missing authorization
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            cur.execute(f"UPDATE payments SET status='refunded' WHERE id={payment_id}")
            conn.commit()
            conn.close()

            return self.send_json({"status": "refunded", "payment_id": payment_id, "refund_amount": amount})

        if path == "/run":
            command = query.get("cmd", ["echo task5-payment"])[0]

            # ZAFİYET-15: Command Injection
            output = subprocess.check_output(command, shell=True, text=True)
            return self.send_json({"command": command, "output": output})

        if path == "/config":
            # ZAFİYET-16: Configuration exposure
            return self.send_json({
                "payment_secret": PAYMENT_SECRET,
                "admin_email": ADMIN_EMAIL,
                "admin_password": ADMIN_PASSWORD,
                "db_name": DB_NAME,
                "cwd": os.getcwd()
            })

        # ZAFİYET-17: Verbose error
        return self.send_json({"error": "Route not found", "path": path}, 404)


if __name__ == "__main__":
    init_db()

    # ZAFİYET-18: Public binding
    HTTPServer(("0.0.0.0", 6601), PaymentHandler).serve_forever()
