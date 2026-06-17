import os
import sqlite3
from pathlib import Path

BASE_PROFILE_DIR = Path("profiles").resolve()

def get_user_by_username(username):
    # PART 1 - SAFE
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    query = "SELECT id, username, email FROM users WHERE username = ?"
    cursor.execute(query, (username,))

    return cursor.fetchone()


def run_report_action(action_name):
    # PART 2 - VULNERABLE: command injection
    command = "python reports.py --type " + action_name
    os.system(command)

    return "Report command executed"


def read_profile_file(filename):
    # PART 3 - SAFE
    requested_path = (BASE_PROFILE_DIR / filename).resolve()

    if not str(requested_path).startswith(str(BASE_PROFILE_DIR)):
        raise ValueError("Invalid file path")

    with open(requested_path, "r", encoding="utf-8") as file:
        return file.read()