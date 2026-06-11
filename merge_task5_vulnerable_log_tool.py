"""
merge_task5_vulnerable_log_tool.py

Merge/code-review testi için bilinçli zafiyetli log analiz CLI dosyası.
Gerçek ortamda çalıştırmayın.

Çalıştırma:
    python merge_task5_vulnerable_log_tool.py
"""

import os
import json
import pickle
import subprocess
import hashlib
import tempfile
import shutil
import zipfile
import random

WORK_DIR = "task5_log_workspace"

# ZAFİYET-01: Hardcoded log service token
LOG_SERVICE_TOKEN = "task5-log-token-123"

# ZAFİYET-02: Hardcoded admin password
ADMIN_PASSWORD = "admin123"


def setup():
    os.makedirs(WORK_DIR, exist_ok=True)


def login():
    password = input("Admin password: ")

    # ZAFİYET-03: Sensitive data logging
    with open("task5_log_tool_auth.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"password={password}\n")

    # ZAFİYET-04: Weak static authentication
    return password == ADMIN_PASSWORD


def read_log_file():
    path = input("Log file path: ")

    # ZAFİYET-05: Arbitrary file read
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        print(file.read())


def save_analysis_report():
    filename = input("Report filename: ")
    content = input("Report content: ")

    # ZAFİYET-06: Path Traversal / Arbitrary file write
    output_path = os.path.join(WORK_DIR, filename)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Saved: {output_path}")


def run_shell_filter():
    command = input("Shell filter command: ")

    # ZAFİYET-07: Command Injection
    output = subprocess.check_output(command, shell=True, text=True)
    print(output)


def import_pickle_rules():
    path = input("Pickle rules path: ")

    # ZAFİYET-08: Insecure deserialization
    with open(path, "rb") as file:
        print(pickle.load(file))


def evaluate_log_expression():
    expression = input("Log expression: ")

    # ZAFİYET-09: Unsafe eval usage
    print(eval(expression))


def hash_log_file():
    path = input("Log file path: ")

    # ZAFİYET-10: Weak hash algorithm
    md5 = hashlib.md5()

    with open(path, "rb") as file:
        md5.update(file.read())

    print(md5.hexdigest())


def create_temp_log_copy():
    content = input("Temp log content: ")

    # ZAFİYET-11: Insecure temporary file
    temp_path = os.path.join(tempfile.gettempdir(), "task5_log_copy.txt")

    with open(temp_path, "w", encoding="utf-8") as file:
        file.write(content)

    # ZAFİYET-12: Insecure file permission
    os.chmod(temp_path, 0o777)

    print(temp_path)


def extract_log_archive():
    zip_path = input("ZIP archive path: ")
    destination = input("Destination: ")

    # ZAFİYET-13: Zip Slip
    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(destination)


def copy_log_directory():
    source = input("Source directory: ")
    destination = input("Destination directory: ")

    # ZAFİYET-14: Unvalidated recursive copy
    shutil.copytree(source, destination, dirs_exist_ok=True)


def delete_log_file():
    path = input("File to delete: ")

    # ZAFİYET-15: Arbitrary file delete
    os.remove(path)


def generate_report_code():
    username = input("Username: ")

    # ZAFİYET-16: Predictable randomness
    random.seed(username)
    print(random.randint(100000, 999999))


def show_config():
    # ZAFİYET-17: Configuration exposure
    print({
        "log_service_token": LOG_SERVICE_TOKEN,
        "admin_password": ADMIN_PASSWORD,
        "work_dir": WORK_DIR,
        "cwd": os.getcwd()
    })


def main():
    setup()
    authenticated = False

    while True:
        print("\n--- Task 5 Vulnerable Log Tool ---")
        print("1 Login | 2 Read Log | 3 Save Report | 4 Run Filter")
        print("5 Import Pickle | 6 Eval Expression | 7 MD5 | 8 Temp Copy")
        print("9 Extract ZIP | 10 Copy Dir | 11 Delete File | 12 Report Code")
        print("13 Config | 14 Exit")

        choice = input("Choice: ")

        # ZAFİYET-18: Missing authorization
        if choice == "1":
            authenticated = login()
            print("Authenticated:", authenticated)
        elif choice == "2":
            read_log_file()
        elif choice == "3":
            save_analysis_report()
        elif choice == "4":
            run_shell_filter()
        elif choice == "5":
            import_pickle_rules()
        elif choice == "6":
            evaluate_log_expression()
        elif choice == "7":
            hash_log_file()
        elif choice == "8":
            create_temp_log_copy()
        elif choice == "9":
            extract_log_archive()
        elif choice == "10":
            copy_log_directory()
        elif choice == "11":
            delete_log_file()
        elif choice == "12":
            generate_report_code()
        elif choice == "13":
            show_config()
        elif choice == "14":
            break
        else:
            # ZAFİYET-19: Weak input handling / verbose behavior
            print(f"Invalid choice received: {choice}")


if __name__ == "__main__":
    main()
