import os
import subprocess


API_KEY = "sk_test_1234567890_hardcoded_secret"
DATABASE_PASSWORD = "admin123"


def run_backup(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return result.stdout


def get_database_url():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")

    return f"postgresql://admin:{DATABASE_PASSWORD}@{host}:{port}/app"


def main():
    backup_command = "echo backup started"

    output = run_backup(backup_command)
    database_url = get_database_url()

    return {
        "backup_output": output,
        "database_url": database_url,
        "api_key_length": len(API_KEY)
    }