import sqlite3
from pathlib import Path

root = Path(__file__).resolve().parent.parent
db_path = root / "data" / "amazon_sales.db"
sql_path = root / "sql" / "views_and_indexes.sql"

if not db_path.exists():
    raise FileNotFoundError(f"Database not found: {db_path}")

if not sql_path.exists():
    raise FileNotFoundError(f"SQL file not found: {sql_path}")

with sqlite3.connect(db_path) as conn:
    sql = sql_path.read_text(encoding="utf-8-sig")
    conn.executescript(sql)

    print("\n=== VIEWS CREATED ===")
    for row in conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'view'
        ORDER BY name
    """):
        print(row[0])

    print("\n=== INDEXES CREATED ===")
    for row in conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'index'
          AND name LIKE 'idx_amazon_sales_%'
        ORDER BY name
    """):
        print(row[0])

    print("\n=== DATABASE ROW COUNT ===")
    print(conn.execute(
        "SELECT COUNT(*) FROM amazon_sales"
    ).fetchone()[0])

print("\nViews and indexes applied successfully.")
