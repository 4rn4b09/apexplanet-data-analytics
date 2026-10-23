# ApexPlanet Data Analytics Internship

A 45-day Data Analytics Internship project focused on data cleaning, exploratory data analysis, SQL querying, database optimization, and Python database integration.

## Project Overview

This repository documents my progress through the ApexPlanet Data Analytics internship. Each task includes relevant notebooks, Python scripts, SQL queries, reports, and visualizations.

## Technologies Used

* Python
* Pandas and NumPy
* Matplotlib and Seaborn
* Jupyter Notebook
* SQLite
* SQLAlchemy
* SQL
* Git and GitHub

## Completed Tasks

### Task 1 — Data Cleaning and Exploratory Data Analysis

**Objective:** Clean the Amazon Sale Report dataset and explore its key characteristics.

Work completed:

* Inspected the dataset and assessed missing values.
* Cleaned and preprocessed data.
* Examined order statuses, product categories, quantities, and recorded sales amounts.
* Created visualizations of product categories and sales trends.

**Notebook:** [`01_data_cleaning_eda.ipynb`](notebooks/01_data_cleaning_eda.ipynb)

**Visualizations:** See the [`visualizations`](visualizations/) folder.

### Task 2 — SQL Analysis and Python Database Integration

**Objective:** Import the cleaned data into SQLite and perform SQL-based analysis.

Work completed:

* Created and populated a SQLite database.
* Executed basic and advanced SQL queries.
* Analyzed monthly trends and product category performance.
* Applied SQL views and indexes.
* Examined query execution plans.
* Connected Python to SQLite using `sqlite3` and SQLAlchemy.
* Used pandas to retrieve query results.
* Tested parameterized queries.
* Documented dataset limitations.

**Notebook:** [`02_advanced_sql_python.ipynb`](notebooks/02_advanced_sql_python.ipynb)

**SQL scripts:** See the [`sql`](sql/) folder.

**Reports:** See the [`reports`](reports/) folder.

### Task Tracker

View [`docs/TASK_TRACKER.md`](docs/TASK_TRACKER.md) for the internship progress checklist.

## Repository Structure

```text
apexplanet-data-analytics/
├── docs/
│   └── TASK_TRACKER.md
├── notebooks/
│   ├── 01_data_cleaning_eda.ipynb
│   └── 02_advanced_sql_python.ipynb
├── scripts/
├── sql/
├── reports/
├── visualizations/
├── data/
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/4rn4b09/apexplanet-data-analytics.git
cd apexplanet-data-analytics
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the database scripts

After placing the required dataset in the expected local `data/` location, run:

```bash
python scripts/create_database.py
python scripts/verify_database.py
python scripts/run_sql_queries.py
```

See the individual scripts and notebooks for further analysis instructions.

## Data Notes

The project uses the Amazon Sale Report dataset. Customer-level retention and revenue rankings cannot be calculated reliably because the available dataset does not contain a customer identifier.

Dataset files and the local SQLite database are excluded from Git tracking. Obtain the dataset from its authorized source and place it in the required local path before running scripts that depend on it.

## Author

**Arnab Sarkar**

Data Analytics Intern | Python | SQL | Exploratory Data Analysis
