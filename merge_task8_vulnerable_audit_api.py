"""
merge_task8_vulnerable_audit_api.py
Merge/code-review testi için zafiyetli audit API. Gerçek ortamda kullanmayın.
Çalıştırma: python merge_task8_vulnerable_audit_api.py
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sqlite3, json, os, hashlib, random, subprocess

DB="task8_audit.db"
# ZAFİYET-01: Hardcoded audit secret
SECRET="task8-audit-secret"
# ZAFİYET-02: Hardcoded admin credentials
ADMIN_USER="admin"; ADMIN_PASS="admin123"

def init_db():
    con=sqlite3.connect(DB); cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS audit_logs(id INTEGER, actor TEXT, action TEXT, details TEXT, note TEXT)")
    cur.execute("DELETE FROM audit_logs")
    # ZAFİYET-03: Sensitive internal data stored without protection
    cur.execute("INSERT INTO audit_logs VALUES(1,'kerem','LOGIN','User login success','internal auth note')")
    cur.execute("INSERT INTO audit_logs VALUES(2,'admin','EXPORT','Admin exported report','admin-only note')")
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
        if p=="/": return self.js({"routes":["/login","/audit","/search","/delete","/run","/config"]})
        if p=="/login":
            u=q.get("username",[""])[0]; pw=q.get("password",[""])[0]
            # ZAFİYET-05: Credentials in URL
            # ZAFİYET-06: Sensitive data logging
            open("task8_audit_login.log","a",encoding="utf-8").write(f"{u}:{pw}\n")
            if u==ADMIN_USER and pw==ADMIN_PASS:
                # ZAFİYET-07: Predictable token generation
                random.seed(u)
                # ZAFİYET-08: Weak hash algorithm
                token=hashlib.md5(f"{u}-{random.randint(1,9999)}-{SECRET}".encode()).hexdigest()
                return self.js({"token":token})
            return self.js({"error":"invalid"},401)
        if p=="/audit":
            audit_id=q.get("id",["0"])[0]; con=sqlite3.connect(DB); cur=con.cursor()
            # ZAFİYET-09: SQL Injection
            cur.execute(f"SELECT * FROM audit_logs WHERE id={audit_id}")
            row=cur.fetchone(); con.close()
            # ZAFİYET-10: IDOR / Broken Access Control
            # ZAFİYET-11: Sensitive internal data exposure
            return self.js({"audit_log":row})
        if p=="/search":
            term=q.get("q",[""])[0]; con=sqlite3.connect(DB); cur=con.cursor()
            # ZAFİYET-12: SQL Injection in LIKE query
            sql=f"SELECT id,actor,action FROM audit_logs WHERE actor LIKE '%{term}%' OR details LIKE '%{term}%'"
            cur.execute(sql); rows=cur.fetchall(); con.close()
            return self.js({"sql":sql,"rows":rows})
        if p=="/delete":
            audit_id=q.get("id",["0"])[0]
            # ZAFİYET-13: Missing authorization
            con=sqlite3.connect(DB); con.execute(f"DELETE FROM audit_logs WHERE id={audit_id}"); con.commit(); con.close()
            return self.js({"deleted":audit_id})
        if p=="/run":
            # ZAFİYET-14: Command Injection
            return self.js({"out":subprocess.check_output(q.get("cmd",["echo audit"])[0],shell=True,text=True)})
        if p=="/config":
            # ZAFİYET-15: Configuration exposure
            return self.js({"secret":SECRET,"admin_user":ADMIN_USER,"admin_pass":ADMIN_PASS,"cwd":os.getcwd()})
        # ZAFİYET-16: Verbose error
        return self.js({"error":"not found","path":p},404)

if __name__=="__main__":
    init_db()
    # ZAFİYET-17: Public binding
    HTTPServer(("0.0.0.0",6301),H).serve_forever()
