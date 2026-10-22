import sqlite3
from pathlib import Path

db_path = Path("data/amazon_sales.db")

if not db_path.exists():
    print("Database file not found!")
else:
    with sqlite3.connect(db_path) as con:
        tables = con.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()

        print("Tables:", tables)

        rows = con.execute(
            "SELECT COUNT(*) FROM amazon_sales"
        ).fetchone()[0]

        print("Total rows:", rows)