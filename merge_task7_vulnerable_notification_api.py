"""
merge_task7_vulnerable_notification_api.py
Merge/code-review testi için zafiyetli notification API. Gerçek ortamda kullanmayın.
Çalıştırma: python merge_task7_vulnerable_notification_api.py
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sqlite3, json, os, hashlib, random, subprocess

DB="task7_notifications.db"
# ZAFİYET-01: Hardcoded notification secret
SECRET="task7-notification-secret"
# ZAFİYET-02: Hardcoded admin credentials
ADMIN_EMAIL="admin@notify.local"; ADMIN_PASSWORD="admin123"

def init_db():
    con=sqlite3.connect(DB); cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS notifications(id INTEGER, user_email TEXT, title TEXT, message TEXT, private_note TEXT)")
    cur.execute("DELETE FROM notifications")
    # ZAFİYET-03: Sensitive notification content stored without protection
    cur.execute("INSERT INTO notifications VALUES(1,'kerem@example.com','Build Failed','Pipeline failed','internal stack trace note')")
    cur.execute("INSERT INTO notifications VALUES(2,'admin@example.com','Security Alert','Sensitive alert','admin-only note')")
    con.commit(); con.close()

class H(BaseHTTPRequestHandler):
    def js(self,d,s=200):
        self.send_response(s); self.send_header("Content-Type","application/json; charset=utf-8")
        # ZAFİYET-04: CORS wildcard
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers(); self.wfile.write(json.dumps(d,indent=2,ensure_ascii=False).encode())
    def html(self,x):
        self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.end_headers(); self.wfile.write(x.encode())
    def pq(self):
        p=urlparse(self.path); return p.path,parse_qs(p.query)
    def do_GET(self):
        p,q=self.pq()
        if p=="/": return self.js({"routes":["/login","/notification","/search","/render","/send","/run","/config"]})
        if p=="/login":
            email=q.get("email",[""])[0]; pw=q.get("password",[""])[0]
            # ZAFİYET-05: Credentials in URL
            # ZAFİYET-06: Sensitive data logging
            open("task7_notification_login.log","a",encoding="utf-8").write(f"{email}:{pw}\n")
            if email==ADMIN_EMAIL and pw==ADMIN_PASSWORD:
                # ZAFİYET-07: Predictable token generation
                random.seed(email)
                # ZAFİYET-08: Weak hash algorithm
                token=hashlib.md5(f"{email}-{random.randint(1,9999)}-{SECRET}".encode()).hexdigest()
                return self.js({"token":token})
            return self.js({"error":"invalid"},401)
        if p=="/notification":
            nid=q.get("id",["0"])[0]; con=sqlite3.connect(DB); cur=con.cursor()
            # ZAFİYET-09: SQL Injection
            cur.execute(f"SELECT * FROM notifications WHERE id={nid}")
            row=cur.fetchone(); con.close()
            # ZAFİYET-10: IDOR / Broken Access Control
            # ZAFİYET-11: Sensitive internal data exposure
            return self.js({"notification":row})
        if p=="/search":
            term=q.get("q",[""])[0]; con=sqlite3.connect(DB); cur=con.cursor()
            # ZAFİYET-12: SQL Injection in LIKE query
            sql=f"SELECT id,user_email,title FROM notifications WHERE title LIKE '%{term}%' OR message LIKE '%{term}%'"
            cur.execute(sql); rows=cur.fetchall(); con.close()
            return self.js({"sql":sql,"rows":rows})
        if p=="/render":
            # ZAFİYET-13: Reflected XSS
            return self.html(f"<h1>{q.get('title',[''])[0]}</h1><p>{q.get('message',[''])[0]}</p>")
        if p=="/send":
            email=q.get("email",[""])[0]; msg=q.get("message",[""])[0]
            # ZAFİYET-14: Missing authorization
            # ZAFİYET-15: No input validation / spam abuse risk
            return self.js({"sent_to":email,"message":msg})
        if p=="/run":
            # ZAFİYET-16: Command Injection
            return self.js({"out":subprocess.check_output(q.get("cmd",["echo notify"])[0],shell=True,text=True)})
        if p=="/config":
            # ZAFİYET-17: Configuration exposure
            return self.js({"secret":SECRET,"admin_email":ADMIN_EMAIL,"admin_password":ADMIN_PASSWORD,"cwd":os.getcwd()})
        # ZAFİYET-18: Verbose error
        return self.js({"error":"not found","path":p},404)

if __name__=="__main__":
    init_db()
    # ZAFİYET-19: Public binding
    HTTPServer(("0.0.0.0",6401),H).serve_forever()
