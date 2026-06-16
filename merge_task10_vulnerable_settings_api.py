"""
merge_task10_vulnerable_settings_api.py
Zafiyetli settings API. Sadece yerel merge/code-review testi içindir.
Çalıştırma: python merge_task10_vulnerable_settings_api.py
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sqlite3, json, os, hashlib, random, subprocess

DB="task10_settings.db"
# ZAFİYET-01: Hardcoded secret
SECRET="task10-settings-secret"
# ZAFİYET-02: Hardcoded admin credentials
ADMIN_USER="admin"; ADMIN_PASS="admin123"

def init_db():
    con=sqlite3.connect(DB); cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS settings(id INTEGER, owner TEXT, key TEXT, value TEXT, note TEXT)")
    cur.execute("DELETE FROM settings")
    # ZAFİYET-03: Sensitive config value stored without protection
    cur.execute("INSERT INTO settings VALUES(1,'kerem','theme','dark','normal note')")
    cur.execute("INSERT INTO settings VALUES(2,'admin','smtp_password','mail-pass-123','admin secret note')")
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
        if p=="/": return self.js({"routes":["/login","/setting","/search","/update","/run","/config"]})
        if p=="/login":
            u=q.get("username",[""])[0]; pw=q.get("password",[""])[0]
            # ZAFİYET-05: Credentials in URL
            # ZAFİYET-06: Sensitive data logging
            open("task10_settings_login.log","a",encoding="utf-8").write(f"{u}:{pw}\n")
            if u==ADMIN_USER and pw==ADMIN_PASS:
                # ZAFİYET-07: Predictable token generation
                random.seed(u)
                # ZAFİYET-08: Weak hash algorithm
                token=hashlib.md5(f"{u}-{random.randint(1,9999)}-{SECRET}".encode()).hexdigest()
                return self.js({"token":token})
            return self.js({"error":"invalid"},401)
        if p=="/setting":
            sid=q.get("id",["0"])[0]; con=sqlite3.connect(DB); cur=con.cursor()
            # ZAFİYET-09: SQL Injection
            cur.execute(f"SELECT * FROM settings WHERE id={sid}")
            row=cur.fetchone(); con.close()
            # ZAFİYET-10: IDOR / Broken Access Control
            # ZAFİYET-11: Sensitive internal data exposure
            return self.js({"setting":row})
        if p=="/search":
            term=q.get("q",[""])[0]; con=sqlite3.connect(DB); cur=con.cursor()
            # ZAFİYET-12: SQL Injection in LIKE query
            sql=f"SELECT id,owner,key,value FROM settings WHERE key LIKE '%{term}%' OR value LIKE '%{term}%'"
            cur.execute(sql); rows=cur.fetchall(); con.close()
            return self.js({"sql":sql,"rows":rows})
        if p=="/update":
            sid=q.get("id",["0"])[0]; value=q.get("value",[""])[0]
            # ZAFİYET-13: Missing authorization
            con=sqlite3.connect(DB); con.execute(f"UPDATE settings SET value='{value}' WHERE id={sid}"); con.commit(); con.close()
            return self.js({"updated":sid})
        if p=="/run":
            # ZAFİYET-14: Command Injection
            return self.js({"out":subprocess.check_output(q.get("cmd",["echo settings"])[0],shell=True,text=True)})
        if p=="/config":
            # ZAFİYET-15: Configuration exposure
            return self.js({"secret":SECRET,"admin_user":ADMIN_USER,"admin_pass":ADMIN_PASS,"cwd":os.getcwd()})
        # ZAFİYET-16: Verbose error
        return self.js({"error":"not found","path":p},404)

if __name__=="__main__":
    init_db()
    # ZAFİYET-17: Public binding
    HTTPServer(("0.0.0.0",6101),H).serve_forever()
