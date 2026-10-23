from pathlib import Path
import nbformat as nbf

root = Path.cwd()
if not (root / "data" / "amazon_sales.db").exists():
    raise FileNotFoundError(
        "Run this script from the apexplanet-data-analytics project folder."
    )

notebook_path = root / "notebooks" / "02_advanced_sql_python.ipynb"
notebook_path.parent.mkdir(parents=True, exist_ok=True)

nb = nbf.v4.new_notebook()
cells = []

def markdown(content):
    cells.append(nbf.v4.new_markdown_cell(content))

def code(content):
    cells.append(nbf.v4.new_code_cell(content))

markdown("""# Task 2: Advanced SQL and Python Database Integration

**Project:** Amazon Sale Report — Data Analytics Internship

This notebook demonstrates SQLite database access, SQL querying, pandas integration,
parameterised queries, analytical window functions, views, and query-plan inspection.

The database contains 128,975 cleaned dataset records. Amount-based results are
labelled as recorded sales because the source includes cancelled and other order
statuses. The dataset has no customer identifier, so customer-level retention
cannot be calculated reliably.
""")

markdown("## 1. Imports and database connection")

code("""from pathlib import Path
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path.cwd()
if not (PROJECT_ROOT / "data" / "amazon_sales.db").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent

DB_PATH = PROJECT_ROOT / "data" / "amazon_sales.db"
assert DB_PATH.exists(), f"Database not found: {DB_PATH}"

engine = create_engine(f"sqlite:///{DB_PATH.as_posix()}")
print("Database:", DB_PATH)
""")

markdown("## 2. Verify the database and inspect its schema")

code("""with sqlite3.connect(DB_PATH) as conn:
    row_count = conn.execute(
        "SELECT COUNT(*) FROM amazon_sales"
    ).fetchone()[0]
    schema = conn.execute(
        "PRAGMA table_info(amazon_sales)"
    ).fetchall()

print("Record count:", row_count)
print("Column names:", [column[1] for column in schema])
assert row_count == 128975
""")

markdown("## 3. Basic SQL: SELECT, WHERE, ORDER BY, and LIMIT")

code("""basic_df = pd.read_sql_query(
    text(\"\"\"
        SELECT order_id, date, category, qty, amount, status
        FROM amazon_sales
        WHERE qty > 1
        ORDER BY amount DESC
        LIMIT :row_limit
    \"\"\"),
    engine,
    params={"row_limit": 10}
)
basic_df
""")

markdown("## 4. Filtering with IN")

code("""in_df = pd.read_sql_query(
    text(\"\"\"
        SELECT category, status, COUNT(*) AS record_count
        FROM amazon_sales
        WHERE category IN (:category1, :category2)
        GROUP BY category, status
        ORDER BY category, record_count DESC
    \"\"\"),
    engine,
    params={"category1": "Set", "category2": "kurta"}
)
in_df
""")

markdown("## 5. Recorded sales by category")

code("""category_df = pd.read_sql_query(
    text(\"\"\"
        SELECT category,
               COUNT(*) AS order_records,
               SUM(qty) AS recorded_quantity,
               ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_sales
        FROM amazon_sales
        GROUP BY category
        ORDER BY recorded_sales DESC
    \"\"\"),
    engine
)
category_df
""")

markdown("## 6. Monthly recorded sales trend")

code("""monthly_df = pd.read_sql_query(
    text(\"\"\"
        SELECT strftime('%Y-%m', date) AS month,
               COUNT(*) AS order_records,
               ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_sales
        FROM amazon_sales
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month
    \"\"\"),
    engine
)
monthly_df
""")

markdown("## 7. Window functions: moving average and cumulative total")

code("""window_df = pd.read_sql_query(
    text(\"\"\"
        WITH monthly AS (
            SELECT strftime('%Y-%m', date) AS month,
                   SUM(COALESCE(amount, 0)) AS recorded_sales
            FROM amazon_sales
            GROUP BY strftime('%Y-%m', date)
        )
        SELECT month,
               ROUND(recorded_sales, 2) AS recorded_sales,
               ROUND(
                   AVG(recorded_sales) OVER (
                       ORDER BY month
                       ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                   ), 2
               ) AS moving_average_3_month,
               ROUND(
                   SUM(recorded_sales) OVER (
                       ORDER BY month
                       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                   ), 2
               ) AS cumulative_recorded_sales
        FROM monthly
        ORDER BY month
    \"\"\"),
    engine
)
window_df
""")

markdown("## 8. Query a reusable database view")

code("""view_df = pd.read_sql_query(
    "SELECT * FROM vw_category_performance ORDER BY recorded_sales DESC",
    engine
)
view_df
""")

markdown("## 9. Parameterised queries and SQL injection safety")

code("""category_parameter = "Set"

safe_df = pd.read_sql_query(
    text(\"\"\"
        SELECT category, COUNT(*) AS record_count
        FROM amazon_sales
        WHERE category = :category
        GROUP BY category
    \"\"\"),
    engine,
    params={"category": category_parameter}
)
safe_df
""")

code("""# This input is passed as a value, not concatenated into SQL.
injection_like_input = "' OR 1=1 --"

safe_test_df = pd.read_sql_query(
    text("SELECT order_id FROM amazon_sales WHERE category = :category"),
    engine,
    params={"category": injection_like_input}
)

print("Rows returned:", len(safe_test_df))
assert len(safe_test_df) == 0
print("PASS: parameterised input did not bypass the filter.")
""")

markdown("## 10. Query optimisation with EXPLAIN QUERY PLAN")

code("""plans = {
    "Date filter": \"\"\"
        SELECT order_id, date, amount
        FROM amazon_sales
        WHERE date = '2022-04-30'
    \"\"\",
    "Category filter": \"\"\"
        SELECT category, COUNT(*)
        FROM amazon_sales
        WHERE category = 'Set'
        GROUP BY category
    \"\"\",
    "Status filter": \"\"\"
        SELECT order_id, status
        FROM amazon_sales
        WHERE status = 'Cancelled'
    \"\"\",
    "SKU lookup": \"\"\"
        SELECT sku, category, amount
        FROM amazon_sales
        WHERE sku = 'SET389-KR-NP-S'
    \"\"\"
}

with sqlite3.connect(DB_PATH) as conn:
    for label, query in plans.items():
        print(f"\\\\n--- {label} ---")
        for plan_row in conn.execute("EXPLAIN QUERY PLAN " + query):
            print(plan_row[-1])
""")

markdown("## 11. JOIN demonstration using monthly aggregate results")

code("""join_df = pd.read_sql_query(
    text(\"\"\"
        WITH monthly_sales AS (
            SELECT strftime('%Y-%m', date) AS month,
                   ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_sales
            FROM amazon_sales
            GROUP BY strftime('%Y-%m', date)
        ),
        monthly_orders AS (
            SELECT strftime('%Y-%m', date) AS month,
                   COUNT(*) AS order_records
            FROM amazon_sales
            GROUP BY strftime('%Y-%m', date)
        )
        SELECT s.month, o.order_records, s.recorded_sales
        FROM monthly_sales AS s
        INNER JOIN monthly_orders AS o ON s.month = o.month
        ORDER BY s.month
    \"\"\"),
    engine
)
join_df
""")

markdown("## 12. Data limitations and conclusions")

markdown("""### Findings and limitations

- The database contains 128,975 records.
- SQL queries demonstrate filtering, sorting, grouping, aggregation, `IN`, `JOIN`,
  views, and window functions.
- Parameterised queries were used instead of string concatenation for user-supplied
  values.
- Index usage was inspected using SQLite's `EXPLAIN QUERY PLAN`.
- The source dataset has an order identifier but no customer identifier. Therefore,
  unique customers, customer retention, and customer-level revenue rankings cannot
  be reliably determined from these fields.
- Recorded amount totals include multiple order statuses unless a query explicitly
  filters them. Missing amounts are treated as zero only for sum calculations;
  this does not recover the missing values.
- The data spans only a limited set of months, so long-term trends should not be
  inferred.

**Conclusion:** SQLite and Python are integrated using SQLAlchemy, pandas, and
sqlite3. The notebook provides a reproducible workflow for Task 2 analysis.
""")

code("""engine.dispose()
print("Notebook analysis completed.")
""")

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {
        "display_name": "Python (analytics)",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "name": "python",
        "version": "3.10"
    }
}

nbf.write(nb, notebook_path)
print(f"Notebook created: {notebook_path}")
print(f"Total cells: {len(cells)}")
