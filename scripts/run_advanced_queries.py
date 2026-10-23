import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "amazon_sales.db"
SQL_PATH = ROOT / "sql" / "advanced_queries.sql"
REPORT_PATH = ROOT / "reports" / "advanced_sql_results.txt"


def load_queries(sql_text):
    """Split SQL into complete statements without breaking comments or strings."""
    statements = []
    buffer = ""

    for line in sql_text.splitlines(keepends=True):
        buffer += line

        if sqlite3.complete_statement(buffer):
            statement = buffer.strip()
            if statement and any(
                not item.strip().startswith("--")
                for item in statement.splitlines()
                if item.strip()
            ):
                statements.append(statement)
            buffer = ""

    if buffer.strip() and any(
        not item.strip().startswith("--")
        for item in buffer.splitlines()
        if item.strip()
    ):
        statements.append(buffer.strip())

    return statements


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    if not SQL_PATH.exists():
        raise FileNotFoundError(f"SQL file not found: {SQL_PATH}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    sql_text = SQL_PATH.read_text(encoding="utf-8-sig")
    queries = load_queries(sql_text)

    connection = sqlite3.connect(DB_PATH)
    report = []

    try:
        total_rows = connection.execute(
            "SELECT COUNT(*) FROM amazon_sales"
        ).fetchone()[0]

        report.append("TASK 2: ADVANCED SQL RESULTS")
        report.append("=" * 70)
        report.append(f"Database records: {total_rows:,}")
        report.append(f"SQL statements detected: {len(queries)}")
        report.append("")

        for number, query in enumerate(queries, start=1):
            cursor = connection.execute(query)
            columns = (
                [description[0] for description in cursor.description]
                if cursor.description
                else []
            )
            rows = cursor.fetchall()

            report.append("-" * 70)
            report.append(f"QUERY {number}")
            report.append("-" * 70)

            if columns:
                report.append(" | ".join(columns))
                report.append("-" * 70)

                for row in rows:
                    report.append(" | ".join(
                        "NULL" if value is None else str(value)
                        for value in row
                    ))

                report.append(f"\nRows returned: {len(rows)}")
            else:
                report.append("Statement executed successfully.")

            report.append("")

            print(
                f"Query {number}/{len(queries)} completed "
                f"({len(rows)} rows returned)."
            )

        report.append("=" * 70)
        report.append("ALL ADVANCED SQL QUERIES EXECUTED SUCCESSFULLY.")

        REPORT_PATH.write_text(
            "\n".join(report) + "\n",
            encoding="utf-8"
        )

        print(f"\nResults saved to: {REPORT_PATH}")
        print(f"Total queries executed: {len(queries)}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
