
import sqlite3
import pandas as pd
from pathlib import Path

# Define database path
PROJECT_DIR = Path(__file__).resolve().parent.parent
db_path = PROJECT_DIR / "data" / "amazon_sales.db"

# Check whether the database exists
if not db_path.exists():
    raise FileNotFoundError(f"Database not found: {db_path}")

print("Connecting to Amazon sales database...")

with sqlite3.connect(db_path) as connection:

    # Query 1: Display the first 10 records
    print("\n--- First 10 Records ---")

    query1 = """
        SELECT *
        FROM amazon_sales
        LIMIT 10
    """

    result = pd.read_sql_query(query1, connection)
    print(result)

    # Query 2: Count total records
    print("\n--- Total Records ---")

    query2 = """
        SELECT COUNT(*) AS total_records
        FROM amazon_sales
    """

    result = pd.read_sql_query(query2, connection)
    print(result)

    # Query 3: List distinct product categories
    print("\n--- Product Categories ---")

    query3 = """
        SELECT DISTINCT category
        FROM amazon_sales
        ORDER BY category
    """

    result = pd.read_sql_query(query3, connection)
    print(result)

    # Query 4: Find records with quantity greater than 1
    print("\n--- Top 10 Records with Quantity > 1 ---")

    query4 = """
        SELECT order_id, category, qty, amount
        FROM amazon_sales
        WHERE qty > 1
        ORDER BY qty DESC
        LIMIT 10
    """

    result = pd.read_sql_query(query4, connection)
    print(result)

    # Query 5: Count records by product category
    print("\n--- Records by Product Category ---")

    query5 = """
        SELECT
            category,
            COUNT(*) AS total_records
        FROM amazon_sales
        GROUP BY category
        ORDER BY total_records DESC
    """

    result = pd.read_sql_query(query5, connection)
    print(result)

    # Query 6: Calculate recorded sales by category
    print("\n--- Recorded Sales by Category ---")

    query6 = """
        SELECT
            category,
            ROUND(SUM(amount), 2) AS total_recorded_sales
        FROM amazon_sales
        GROUP BY category
        ORDER BY total_recorded_sales DESC
    """

    result = pd.read_sql_query(query6, connection)
    print(result)

    # Query 7: Analyze order statuses
    print("\n--- Order Status Analysis ---")

    query7 = """
        SELECT
            status,
            COUNT(*) AS total_records,
            ROUND(
                COUNT(*) * 100.0 /
                (SELECT COUNT(*) FROM amazon_sales),
                2
            ) AS percentage
        FROM amazon_sales
        GROUP BY status
        ORDER BY total_records DESC
    """

    result = pd.read_sql_query(query7, connection)
    print(result)

    # Query 8: Calculate average amount by category
    print("\n--- Average Amount by Category ---")

    query8 = """
        SELECT
            category,
            ROUND(AVG(amount), 2) AS average_amount,
            COUNT(amount) AS records_with_amount
        FROM amazon_sales
        GROUP BY category
        ORDER BY average_amount DESC
    """

    result = pd.read_sql_query(query8, connection)
    print(result)

    # Query 9: Find the 10 records with the highest amounts
    print("\n--- Top 10 Records by Amount ---")

    query9 = """
        SELECT order_id, category, amount, status
        FROM amazon_sales
        WHERE amount IS NOT NULL
        ORDER BY amount DESC
        LIMIT 10
    """

    result = pd.read_sql_query(query9, connection)
    print(result)

    # Query 10: Analyze quantity by category
    print("\n--- Quantity Analysis by Category ---")

    query10 = """
        SELECT
            category,
            SUM(qty) AS total_quantity,
            ROUND(AVG(qty), 2) AS average_quantity,
            MAX(qty) AS maximum_quantity
        FROM amazon_sales
        GROUP BY category
        ORDER BY total_quantity DESC
    """

    result = pd.read_sql_query(query10, connection)
    print(result)

    # Query 11: Count cancelled records by category
    print("\n--- Cancelled Records by Category ---")

    query11 = """
        SELECT
            category,
            COUNT(*) AS cancelled_records,
            ROUND(
                COUNT(*) * 100.0 /
                (SELECT COUNT(*)
                 FROM amazon_sales
                 WHERE status = 'Cancelled'),
                2
            ) AS percentage_of_cancellations
        FROM amazon_sales
        WHERE status = 'Cancelled'
        GROUP BY category
        ORDER BY cancelled_records DESC
    """

    result = pd.read_sql_query(query11, connection)
    print(result)

    # Query 12: Calculate cancellation rate by category
    print("\n--- Cancellation Rate by Category ---")

    query12 = """
        SELECT
            category,
            COUNT(*) AS total_records,
            SUM(
                CASE
                    WHEN status = 'Cancelled' THEN 1
                    ELSE 0
                END
            ) AS cancelled_records,
            ROUND(
                SUM(
                    CASE
                        WHEN status = 'Cancelled' THEN 1.0
                        ELSE 0
                    END
                ) * 100.0 / COUNT(*),
                2
            ) AS cancellation_rate
        FROM amazon_sales
        GROUP BY category
        ORDER BY cancellation_rate DESC
    """

    result = pd.read_sql_query(query12, connection)
    print(result)

# Query 13: Recorded sales amount by order status
print("\n--- Query 13: Recorded Sales Amount by Order Status ---")

query13 = """
    SELECT
        status,
        COUNT(*) AS total_records,
        ROUND(SUM(amount), 2) AS total_recorded_amount,
        ROUND(AVG(amount), 2) AS average_recorded_amount
    FROM amazon_sales
    GROUP BY status
    ORDER BY total_recorded_amount DESC
"""

result = pd.read_sql_query(query13, connection)
print(result)

connection.close()

print("\nAll 13 SQL queries executed successfully!")

