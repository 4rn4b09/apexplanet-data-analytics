import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "data" / "amazon_sales.db"

with sqlite3.connect(db_path) as conn:
    conn.execute("ANALYZE")

    queries = {
        "Date filter": """
            SELECT order_id, date, amount
            FROM amazon_sales
            WHERE date = '2022-04-30'
        """,
        "Category filter": """
            SELECT category, COUNT(*)
            FROM amazon_sales
            WHERE category = 'Set'
            GROUP BY category
        """,
        "Status filter": """
            SELECT order_id, status
            FROM amazon_sales
            WHERE status = 'Cancelled'
        """,
        "SKU lookup": """
            SELECT sku, category, amount
            FROM amazon_sales
            WHERE sku = 'SET389-KR-NP-S'
        """
    }

    for name, query in queries.items():
        print(f"\n=== {name} ===")
        for row in conn.execute("EXPLAIN QUERY PLAN " + query):
            print(row)

print("\nQuery-plan analysis completed.")
