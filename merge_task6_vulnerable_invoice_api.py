"""
merge_task6_vulnerable_invoice_api.py
Merge/code-review testi için zafiyetli invoice API. Gerçek ortamda kullanmayın.
Çalıştırma: python merge_task6_vulnerable_invoice_api.py
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sqlite3, json, os, hashlib, random, subprocess

DB="task6_invoice.db"
# ZAFİYET-01: Hardcoded secret
SECRET="task6-invoice-secret"
# ZAFİYET-02: Hardcoded admin credentials
ADMIN_EMAIL="admin@invoice.local"; ADMIN_PASSWORD="admin123"

def init_db():
    con=sqlite3.connect(DB); cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS invoices(id INTEGER, email TEXT, amount REAL, status TEXT, note TEXT)")
    cur.execute("DELETE FROM invoices")
    # ZAFİYET-03: Sensitive billing data stored without protection
    cur.execute("INSERT INTO invoices VALUES(1,'kerem@example.com',1500,'paid','internal accounting note')")
    cur.execute("INSERT INTO invoices VALUES(2,'admin@example.com',9900,'pending','admin-only note')")
    con.commit(); con.close()

class H(BaseHTTPRequestHandler):
    def js(self,d,s=200):
        self.send_response(s); self.send_header("Content-Type","application/json; charset=utf-8")
        # ZAFİYET-04: CORS wildcard
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers(); self.wfile.write(json.dumps(d,indent=2,ensure_ascii=False).encode())
    def pq(self):
        p=urlparse(self.path); return p.path,parse_qs(p.query)
    def do_GET(self):
        p,q=self.pq()
        if p=="/": return self.js({"routes":["/login","/invoice","/search","/pay","/run","/config"]})
        if p=="/login":
            email=q.get("email",[""])[0]; pw=q.get("password",[""])[0]
            # ZAFİYET-05: Credentials in URL
            # ZAFİYET-06: Sensitive data logging
            open("task6_invoice_login.log","a",encoding="utf-8").write(f"{email}:{pw}\n")
            if email==ADMIN_EMAIL and pw==ADMIN_PASSWORD:
                # ZAFİYET-07: Predictable token generation
                random.seed(email)
                # ZAFİYET-08: Weak hash algorithm
                token=hashlib.md5(f"{email}-{random.randint(1,9999)}-{SECRET}".encode()).hexdigest()
                return self.js({"token":token})
            return self.js({"error":"invalid"},401)
        if p=="/invoice":
            invoice_id=q.get("id",["0"])[0]; con=sqlite3.connect(DB); cur=con.cursor()
            # ZAFİYET-09: SQL Injection
            cur.execute(f"SELECT * FROM invoices WHERE id={invoice_id}")
            row=cur.fetchone(); con.close()
            # ZAFİYET-10: IDOR / Broken Access Control
            # ZAFİYET-11: Sensitive internal data exposure
            return self.js({"invoice":row})
        if p=="/search":
            term=q.get("q",[""])[0]; con=sqlite3.connect(DB); cur=con.cursor()
            # ZAFİYET-12: SQL Injection in LIKE query
            sql=f"SELECT id,email,amount,status FROM invoices WHERE email LIKE '%{term}%'"
            cur.execute(sql); rows=cur.fetchall(); con.close()
            return self.js({"sql":sql,"rows":rows})
        if p=="/pay":
            invoice_id=q.get("id",["0"])[0]; amount=q.get("amount",["0"])[0]
            # ZAFİYET-13: Business logic flaw, tutar kullanıcıdan geliyor
            # ZAFİYET-14: Missing authorization
            con=sqlite3.connect(DB); con.execute(f"UPDATE invoices SET status='paid', amount={amount} WHERE id={invoice_id}"); con.commit(); con.close()
            return self.js({"paid":invoice_id,"amount":amount})
        if p=="/run":
            # ZAFİYET-15: Command Injection
            return self.js({"out":subprocess.check_output(q.get("cmd",["echo invoice"])[0],shell=True,text=True)})
        if p=="/config":
            # ZAFİYET-16: Configuration exposure
            return self.js({"secret":SECRET,"admin_email":ADMIN_EMAIL,"admin_password":ADMIN_PASSWORD,"cwd":os.getcwd()})
        # ZAFİYET-17: Verbose error
        return self.js({"error":"not found","path":p},404)

if __name__=="__main__":
    init_db()
    # ZAFİYET-18: Public binding
    HTTPServer(("0.0.0.0",6501),H).serve_forever()
