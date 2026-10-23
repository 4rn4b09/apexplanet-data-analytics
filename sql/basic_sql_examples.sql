-- Task 2: Basic SQL examples
-- Database: SQLite | Table: amazon_sales

-- 1. SELECT: retrieve selected columns
SELECT order_id, date, category, amount
FROM amazon_sales;

-- 2. WHERE: filter records
SELECT order_id, category, amount
FROM amazon_sales
WHERE amount > 1000;

-- 3. ORDER BY: sort recorded amounts
SELECT order_id, category, amount
FROM amazon_sales
WHERE amount IS NOT NULL
ORDER BY amount DESC;

-- 4. LIMIT: return the first 10 records
SELECT order_id, date, category, amount
FROM amazon_sales
ORDER BY date DESC
LIMIT 10;

-- 5. IN: filter for selected categories
SELECT order_id, category, status, amount
FROM amazon_sales
WHERE category IN ('Set', 'kurta');

-- 6. JOIN: combine monthly sales and order-count aggregates.
-- Both aggregates are derived from the same source table.
WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', date) AS month,
        ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_sales
    FROM amazon_sales
    GROUP BY strftime('%Y-%m', date)
),
monthly_orders AS (
    SELECT
        strftime('%Y-%m', date) AS month,
        COUNT(*) AS order_records
    FROM amazon_sales
    GROUP BY strftime('%Y-%m', date)
)
SELECT
    s.month,
    o.order_records,
    s.recorded_sales
FROM monthly_sales AS s
INNER JOIN monthly_orders AS o
    ON s.month = o.month
ORDER BY s.month;
