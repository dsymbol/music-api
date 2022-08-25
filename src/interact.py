import os
import sqlite3
from pathlib import Path

DATABASE_PATH = os.path.join(str(Path(__file__).parents[1]), "music.db")

conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
c = conn.cursor()


def query(statement: str, *args):
    if not os.path.exists(DATABASE_PATH):
        raise Exception("Database file not found")

    with conn:
        if "select" in statement.lower():
            c.execute(statement, args)
            result = c.fetchall()
        else:
            c.execute("PRAGMA foreign_keys = ON")
            c.execute(statement, args)
            result = c.rowcount
    return result
