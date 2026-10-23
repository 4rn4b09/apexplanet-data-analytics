# ApexPlanet Data Analytics Internship

**45-Day Data Analytics Internship Project** at ApexPlanet Software Pvt. Ltd.

This repository covers data cleaning, exploratory data analysis (EDA), SQL analysis, database optimization, and Python database integration.

## Task 1 — Data Cleaning and EDA

- Cleaned and inspected the Amazon Sale Report dataset.
- Examined missing values, order statuses, quantities, categories, and recorded sales.
- Created visualizations for categories, recorded sales amounts, and daily/monthly trends.

## Task 2 — SQL and Database Analysis

- Imported 128,975 records into a local SQLite database.
- Demonstrated SELECT, WHERE, ORDER BY, LIMIT, IN, and JOIN.
- Analyzed monthly trends, product categories, order statuses, cancellations, and shipping states.
- Used moving averages and cumulative sums.
- Created SQL views and indexes.
- Examined query plans using EXPLAIN QUERY PLAN.

## Python Database Integration

- SQLite3 connections and SQLAlchemy.
- pandas SQL queries and DataFrames.
- Parameterized queries and reusable database functions.
- Integration tests for database access and parameter handling.

The psycopg2-binary PostgreSQL driver is installed, but a live PostgreSQL connection has not been tested.

## Project Structure

- data/ — datasets and local database, excluded from Git.
- notebooks/ — analysis notebooks.
- scripts/ — database setup, SQL analysis, optimization, and tests.
- sql/ — SQL query files.
- reports/ — query results and data limitations.
- visualizations/ — exploratory analysis charts.

## Setup

Install dependencies using:

    pip install -r requirements.txt

The cleaned CSV must exist at data/Amazon_Sale_Report_Cleaned.csv before creating the database.

## Run the Analysis

Run these commands from the repository root:

    python scripts/create_database.py
    python scripts/verify_database.py
    python scripts/run_sql_queries.py
    python scripts/test_basic_sql.py
    python scripts/run_advanced_queries.py
    python scripts/apply_views_and_indexes.py
    python scripts/analyze_query_plans.py
    python scripts/test_database_integration.py

Open the advanced notebook:

    jupyter notebook notebooks/02_advanced_sql_python.ipynb

## Data Limitations

- The dataset has no customer_id, so customer retention and customer-level revenue rankings cannot be calculated reliably.
- order_id identifies an order, not a customer.
- Missing amounts are preserved rather than guessed.
- Recorded sales totals may include cancelled or other non-completed orders unless statuses are filtered.
- The dataset covers March through June 2022, with substantially fewer records in March.

See reports/data_limitations.md for further details.

## Technologies

Python, pandas, NumPy, SQLite, SQL, SQLAlchemy, psycopg2-binary, Jupyter Notebook, Matplotlib, Seaborn, Plotly, Git, and GitHub.

## Project Status

- Task 1: Data cleaning and exploratory data analysis completed.
- Task 2: SQL analysis, Python integration, and query-plan checks completed.

This project is for educational and internship purposes.
