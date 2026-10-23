import sqlite3

conn = sqlite3.connect("data/amazon_sales.db")

print("\n=== DATABASE TABLES ===")
for row in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
):
    print(row)

print("\n=== TABLE COLUMNS ===")
for row in conn.execute("PRAGMA table_info(amazon_sales)"):
    print(row)

print("\n=== TOTAL ROWS ===")
print(conn.execute("SELECT COUNT(*) FROM amazon_sales").fetchone())

print("\n=== SAMPLE RECORDS ===")
for row in conn.execute("SELECT * FROM amazon_sales LIMIT 3"):
    print(row)

conn.close()
