import sqlite3
from pathlib import Path

root = Path(__file__).resolve().parent.parent
db_path = root / "data" / "amazon_sales.db"
sql_path = root / "sql" / "basic_sql_examples.sql"

if not db_path.exists():
    raise FileNotFoundError(f"Database not found: {db_path}")
if not sql_path.exists():
    raise FileNotFoundError(f"SQL file not found: {sql_path}")

sql_text = sql_path.read_text(encoding="utf-8-sig")

# Separate the file into individual SQL statements, ignoring comments.
statements = []
buffer = ""

for line in sql_text.splitlines():
    if line.strip().startswith("--"):
        continue
    buffer += line + "\n"
    if sqlite3.complete_statement(buffer):
        if buffer.strip():
            statements.append(buffer.strip())
        buffer = ""

if buffer.strip():
    raise ValueError("The SQL file contains an incomplete statement.")

with sqlite3.connect(db_path) as conn:
    for number, statement in enumerate(statements, start=1):
        cursor = conn.execute(statement)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description or []]

        print(f"\n=== Query {number}/{len(statements)} ===")
        print("Columns:", ", ".join(columns))
        print("Rows returned:", len(rows))

        for row in rows[:5]:
            print(row)

print(f"\nSUCCESS: Executed all {len(statements)} SQL examples.")
