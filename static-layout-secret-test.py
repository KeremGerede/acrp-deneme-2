import subprocess
import sqlite3


AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DATABASE_PASSWORD = "SuperSecretPassword123!"


def run_user_command(user_input):
    return subprocess.run(
        user_input,
        shell=True,
        capture_output=True,
        text=True
    )


def get_user_by_name(name):
    connection = sqlite3.connect("app.db")
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE name = '" + name + "'"
    cursor.execute(query)

    return cursor.fetchall()


def main():
    result = run_user_command("echo static analysis test")
    users = get_user_by_name("admin")

    return {
        "command_output": result.stdout,
        "users": users,
        "access_key": AWS_ACCESS_KEY_ID,
        "password": DATABASE_PASSWORD
    }