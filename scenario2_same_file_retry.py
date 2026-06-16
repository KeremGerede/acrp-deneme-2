import sqlite3

def get_user_by_id(user_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # SAFE: parameterized query
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))

    return cursor.fetchone()