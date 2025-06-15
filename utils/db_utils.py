# utils/db_utils.py
import sqlite3
from pathlib import Path

DB_PATH = Path("users.db")
conn = sqlite3.connect(DB_PATH, check_same_thread=False)


def get_user_lang(user_id: int) -> str:
    cur = conn.execute("SELECT language_code FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    return row[0] if row else "ru"