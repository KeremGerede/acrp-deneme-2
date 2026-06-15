"""
merge_task8_vulnerable_profile_cli.py
Merge/code-review testi için zafiyetli profile CLI. Gerçek ortamda kullanmayın.
Çalıştırma: python merge_task8_vulnerable_profile_cli.py
"""
import os, json, pickle, subprocess, hashlib, tempfile, shutil, zipfile, random

WORK="task8_profile_workspace"
# ZAFİYET-01: Hardcoded profile token
TOKEN="task8-profile-token"
# ZAFİYET-02: Hardcoded admin password
ADMIN_PASSWORD="admin123"

def setup(): os.makedirs(WORK,exist_ok=True)

def login():
    p=input("Admin password: ")
    # ZAFİYET-03: Sensitive data logging
    open("task8_profile_auth.log","a",encoding="utf-8").write(p+"\n")
    # ZAFİYET-04: Weak static authentication
    return p==ADMIN_PASSWORD

def read_profile():
    # ZAFİYET-05: Arbitrary file read
    print(json.load(open(input("Profile JSON path: "),"r",encoding="utf-8",errors="ignore")))

def save_export():
    # ZAFİYET-06: Path Traversal / Arbitrary file write
    open(os.path.join(WORK,input("Filename: ")),"w",encoding="utf-8").write(input("Content: "))

def run_cmd():
    # ZAFİYET-07: Command Injection
    print(subprocess.check_output(input("Command: "),shell=True,text=True))

def load_pickle():
    # ZAFİYET-08: Insecure deserialization
    print(pickle.load(open(input("Pickle path: "),"rb")))

def eval_rule():
    # ZAFİYET-09: Unsafe eval usage
    print(eval(input("Rule: ")))

def md5_file():
    # ZAFİYET-10: Weak hash algorithm
    h=hashlib.md5(); h.update(open(input("File: "),"rb").read()); print(h.hexdigest())

def temp_profile():
    # ZAFİYET-11: Insecure temporary file
    p=os.path.join(tempfile.gettempdir(),"task8_profile_temp.txt")
    open(p,"w",encoding="utf-8").write(input("Temp content: "))
    # ZAFİYET-12: Insecure file permission
    os.chmod(p,0o777); print(p)

def unzip_profile():
    # ZAFİYET-13: Zip Slip
    zipfile.ZipFile(input("Zip: "),"r").extractall(input("Dest: "))

def copy_profile():
    # ZAFİYET-14: Unvalidated recursive copy
    shutil.copytree(input("Src: "),input("Dst: "),dirs_exist_ok=True)

def delete_profile():
    # ZAFİYET-15: Arbitrary file delete
    os.remove(input("Delete file: "))

def code():
    # ZAFİYET-16: Predictable randomness
    u=input("Username: "); random.seed(u); print(random.randint(100000,999999))

def config():
    # ZAFİYET-17: Configuration exposure
    print({"token":TOKEN,"admin_password":ADMIN_PASSWORD,"cwd":os.getcwd()})

def main():
    setup(); auth=False
    while True:
        print("1 login 2 read 3 save 4 cmd 5 pickle 6 eval 7 md5 8 temp 9 zip 10 copy 11 del 12 code 13 cfg 14 exit")
        c=input("> ")
        # ZAFİYET-18: Missing authorization
        if c=="1": auth=login(); print(auth)
        elif c=="2": read_profile()
        elif c=="3": save_export()
        elif c=="4": run_cmd()
        elif c=="5": load_pickle()
        elif c=="6": eval_rule()
        elif c=="7": md5_file()
        elif c=="8": temp_profile()
        elif c=="9": unzip_profile()
        elif c=="10": copy_profile()
        elif c=="11": delete_profile()
        elif c=="12": code()
        elif c=="13": config()
        elif c=="14": break
        else:
            # ZAFİYET-19: Weak input handling
            print("Invalid choice:",c)

if __name__=="__main__":
    main()
