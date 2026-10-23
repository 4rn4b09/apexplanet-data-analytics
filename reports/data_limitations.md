# Task 2 — Dataset Limitations and Analysis Notes

## 1. Missing Customer Identifier
The Amazon Sale Report dataset does not contain a customer_id field.
Therefore, customer-level revenue rankings, repeat-customer analysis,
and customer retention rates cannot be calculated reliably.

The order_id field identifies an order, not necessarily a unique customer.
It must not be used as a substitute for customer_id.

## 2. Revenue Interpretation
The amount column contains missing values. These values are preserved
rather than guessed during data cleaning.

Sales totals should be described as recorded sales amounts. Unless a
query explicitly filters order statuses, totals may include cancelled
or other non-completed orders.

Where COALESCE(amount, 0) is used, missing amounts contribute zero to
the calculation. This is a calculation choice, not proof that the
actual transaction value was zero.

## 3. Date Coverage
The available records cover March through June 2022, with very few
records in March compared with April, May, and June.

Monthly comparisons should consider this uneven date coverage.
The dataset cannot support conclusions about a full year or current
sales performance.

## 4. Zero-Value Records
Zero amounts and zero quantities are retained in the cleaned dataset.
They may represent cancellations or other business cases and should
not be removed without a documented reason.

## 5. Valid Alternatives
Although customer-level analysis is not possible, this project
includes:
- Monthly recorded sales trends.
- Category-level performance.
- Top products/SKUs by recorded sales amount.
- Order-status and cancellation analysis.
- Shipping-state summaries.
- Moving averages and cumulative recorded sales.
- SQL views, indexes, and query-plan analysis.

## 6. Database and Python Integration
The project uses SQLite for the local database and demonstrates
SQLite3, SQLAlchemy, pandas SQL reading, and parameterized queries.

The psycopg2-binary package is installed as a PostgreSQL driver.
A live PostgreSQL connection has not been verified as part of this
SQLite-based project.

## Conclusion
The analysis reports only what the available fields support. Missing
customer identifiers and incomplete transaction values are documented
rather than replaced with unsupported assumptions.
