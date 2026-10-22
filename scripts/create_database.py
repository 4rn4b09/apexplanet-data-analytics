
import sqlite3
import pandas as pd
from pathlib import Path

# Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
csv_path = PROJECT_DIR / "data" / "Amazon_Sale_Report_Cleaned.csv"
db_path = PROJECT_DIR / "data" / "amazon_sales.db"

# Check whether the cleaned CSV exists
if not csv_path.exists():
    raise FileNotFoundError(f"Cleaned CSV not found: {csv_path}")

print("Loading cleaned Amazon sales data...")

# Create the database and import the data
with sqlite3.connect(db_path) as connection:
    df = pd.read_csv(csv_path, low_memory=False)

    df.to_sql(
        "amazon_sales",
        connection,
        if_exists="replace",
        index=False
    )

    count = connection.execute(
        "SELECT COUNT(*) FROM amazon_sales"
    ).fetchone()[0]

    print(f"Database created: {db_path}")
    print(f"Rows imported: {count:,}")
    print("Table name: amazon_sales")
    print("Database creation completed successfully!")

