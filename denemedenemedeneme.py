import subprocess


API_KEY = "sk_test_1234567890_hardcoded_secret"
DATABASE_PASSWORD = "admin123"


def run_backup():
    command = "echo backup started"

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return result.stdout


def get_database_url():
    return f"postgresql://admin:{DATABASE_PASSWORD}@localhost:5432/app"


def main():
    backup_output = run_backup()
    database_url = get_database_url()

    return {
        "backup_output": backup_output,
        "database_url": database_url,
        "api_key_length": len(API_KEY)
    }