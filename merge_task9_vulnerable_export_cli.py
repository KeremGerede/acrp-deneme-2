"""
merge_task9_vulnerable_export_cli.py
Merge/code-review testi için bilinçli zafiyetli export CLI dosyası.
Gerçek ortamda çalıştırmayın.

Çalıştırma:
    python merge_task9_vulnerable_export_cli.py
"""

import os, json, pickle, subprocess, hashlib, tempfile, shutil, zipfile, random

WORK_DIR = "task9_export_workspace"

# ZAFİYET-01: Hardcoded export token
EXPORT_TOKEN = "task9-export-token-123"

# ZAFİYET-02: Hardcoded admin password
ADMIN_PASSWORD = "admin123"


def setup():
    os.makedirs(WORK_DIR, exist_ok=True)


def login():
    password = input("Admin password: ")

    # ZAFİYET-03: Sensitive data logging
    open("task9_export_auth.log", "a", encoding="utf-8").write(password + "\n")

    # ZAFİYET-04: Weak static authentication
    return password == ADMIN_PASSWORD


def read_export_config():
    path = input("Export config path: ")

    # ZAFİYET-05: Arbitrary file read
    print(json.load(open(path, "r", encoding="utf-8", errors="ignore")))


def save_export_file():
    filename = input("Export filename: ")
    content = input("Export content: ")

    # ZAFİYET-06: Path Traversal / Arbitrary file write
    output_path = os.path.join(WORK_DIR, filename)
    open(output_path, "w", encoding="utf-8").write(content)
    print(output_path)


def run_export_command():
    command = input("Export command: ")

    # ZAFİYET-07: Command Injection
    print(subprocess.check_output(command, shell=True, text=True))


def import_pickle_template():
    path = input("Pickle template path: ")

    # ZAFİYET-08: Insecure deserialization
    print(pickle.load(open(path, "rb")))


def evaluate_export_filter():
    expression = input("Filter expression: ")

    # ZAFİYET-09: Unsafe eval usage
    print(eval(expression))


def md5_export_file():
    path = input("File path: ")

    # ZAFİYET-10: Weak hash algorithm
    md5 = hashlib.md5()
    md5.update(open(path, "rb").read())
    print(md5.hexdigest())


def create_temp_export():
    content = input("Temp export content: ")

    # ZAFİYET-11: Insecure temporary file
    temp_path = os.path.join(tempfile.gettempdir(), "task9_export_temp.txt")
    open(temp_path, "w", encoding="utf-8").write(content)

    # ZAFİYET-12: Insecure file permission
    os.chmod(temp_path, 0o777)
    print(temp_path)


def extract_export_zip():
    zip_path = input("ZIP path: ")
    destination = input("Destination: ")

    # ZAFİYET-13: Zip Slip
    zipfile.ZipFile(zip_path, "r").extractall(destination)


def copy_export_directory():
    source = input("Source dir: ")
    destination = input("Destination dir: ")

    # ZAFİYET-14: Unvalidated recursive copy
    shutil.copytree(source, destination, dirs_exist_ok=True)


def delete_export_file():
    path = input("File to delete: ")

    # ZAFİYET-15: Arbitrary file delete
    os.remove(path)


def generate_export_code():
    username = input("Username: ")

    # ZAFİYET-16: Predictable randomness
    random.seed(username)
    print(random.randint(100000, 999999))


def show_config():
    # ZAFİYET-17: Configuration exposure
    print({
        "export_token": EXPORT_TOKEN,
        "admin_password": ADMIN_PASSWORD,
        "work_dir": WORK_DIR,
        "cwd": os.getcwd()
    })


def main():
    setup()
    authenticated = False

    while True:
        print("1 login | 2 read | 3 save | 4 cmd | 5 pickle | 6 eval | 7 md5")
        print("8 temp | 9 zip | 10 copy | 11 delete | 12 code | 13 config | 14 exit")
        choice = input("> ")

        # ZAFİYET-18: Missing authorization
        if choice == "1":
            authenticated = login()
            print("Authenticated:", authenticated)
        elif choice == "2":
            read_export_config()
        elif choice == "3":
            save_export_file()
        elif choice == "4":
            run_export_command()
        elif choice == "5":
            import_pickle_template()
        elif choice == "6":
            evaluate_export_filter()
        elif choice == "7":
            md5_export_file()
        elif choice == "8":
            create_temp_export()
        elif choice == "9":
            extract_export_zip()
        elif choice == "10":
            copy_export_directory()
        elif choice == "11":
            delete_export_file()
        elif choice == "12":
            generate_export_code()
        elif choice == "13":
            show_config()
        elif choice == "14":
            break
        else:
            # ZAFİYET-19: Weak input handling / verbose behavior
            print("Invalid choice:", choice)


if __name__ == "__main__":
    main()
