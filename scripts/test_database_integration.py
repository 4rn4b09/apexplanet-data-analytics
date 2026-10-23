import sqlite3
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from database_utils import DATABASE_PATH, get_engine, get_sqlite_connection, read_query

print("=== 1. SQLite3 connection ===")
with get_sqlite_connection() as conn:
    count = conn.execute("SELECT COUNT(*) FROM amazon_sales").fetchone()[0]
    print("Database row count:", count)

print("\n=== 2. SQLAlchemy connection ===")
engine = get_engine()
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM amazon_sales")).scalar_one()
    print("SQLAlchemy row count:", result)
engine.dispose()

print("\n=== 3. pandas DataFrame ===")
df = read_query(
    "SELECT category, COUNT(*) AS records FROM amazon_sales GROUP BY category ORDER BY records DESC LIMIT :limit",
    {"limit": 5},
)
print(df.to_string(index=False))
print("Returned a pandas DataFrame:", isinstance(df, pd.DataFrame))

print("\n=== 4. Parameterised filter ===")
test_value = "' OR 1=1 --"
filtered = read_query(
    "SELECT order_id FROM amazon_sales WHERE category = :category LIMIT 5",
    {"category": test_value},
)
print("Rows returned for injection-like input:", len(filtered))
print("The input was treated as a value, not SQL code.")

print("\n=== 5. Checks ===")
assert count == 128975, f"Unexpected SQLite row count: {count}"
assert result == count, "SQLite3 and SQLAlchemy counts differ."
assert isinstance(df, pd.DataFrame), "Query result is not a DataFrame."
assert len(filtered) == 0, "Unexpected match for injection-like input."

print("ALL INTEGRATION TESTS PASSED.")
