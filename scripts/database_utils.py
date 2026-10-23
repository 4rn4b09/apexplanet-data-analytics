"""Reusable database utilities for the Amazon sales analysis project."""

import sqlite3
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "amazon_sales.db"


def get_engine():
    """Create a SQLAlchemy engine for the local SQLite database."""
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")
    return create_engine(f"sqlite:///{DATABASE_PATH.as_posix()}")


def get_sqlite_connection():
    """Return a standard sqlite3 connection."""
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")
    return sqlite3.connect(DATABASE_PATH)


def read_query(query, params=None):
    """Execute a parameterised read query and return a DataFrame."""
    engine = get_engine()
    try:
        with engine.connect() as connection:
            return pd.read_sql_query(
                text(query),
                connection,
                params=params or {}
            )
    finally:
        engine.dispose()


if __name__ == "__main__":
    df = read_query(
        """
        SELECT category, COUNT(*) AS record_count
        FROM amazon_sales
        GROUP BY category
        ORDER BY record_count DESC
        LIMIT :limit
        """,
        {"limit": 5}
    )

    print("Top 5 categories by record count:")
    print(df.to_string(index=False))
    print("\nDatabase utilities test completed.")
