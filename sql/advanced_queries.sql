-- =========================================================
-- TASK 2: ADVANCED SQL ANALYSIS
-- Dataset: Amazon Sales Report
-- Database: SQLite
-- =========================================================

-- Query 1: Monthly order-record count and recorded sales amount
SELECT
    strftime('%Y-%m', date) AS month,
    COUNT(*) AS order_records,
    ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_sales_amount
FROM amazon_sales
GROUP BY strftime('%Y-%m', date)
ORDER BY month;


-- Query 2: Monthly recorded sales with a three-month moving average
WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', date) AS month,
        SUM(COALESCE(amount, 0)) AS recorded_sales
    FROM amazon_sales
    GROUP BY strftime('%Y-%m', date)
)
SELECT
    month,
    ROUND(recorded_sales, 2) AS recorded_sales,
    ROUND(
        AVG(recorded_sales) OVER (
            ORDER BY month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS three_month_moving_average
FROM monthly_sales
ORDER BY month;


-- Query 3: Monthly recorded sales and cumulative total
WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', date) AS month,
        SUM(COALESCE(amount, 0)) AS recorded_sales
    FROM amazon_sales
    GROUP BY strftime('%Y-%m', date)
)
SELECT
    month,
    ROUND(recorded_sales, 2) AS recorded_sales,
    ROUND(
        SUM(recorded_sales) OVER (
            ORDER BY month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS cumulative_recorded_sales
FROM monthly_sales
ORDER BY month;


-- Query 4: Product category performance
SELECT
    category,
    COUNT(*) AS record_count,
    SUM(qty) AS total_recorded_quantity,
    ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_sales_amount,
    ROUND(AVG(amount), 2) AS average_recorded_amount
FROM amazon_sales
GROUP BY category
ORDER BY recorded_sales_amount DESC;


-- Query 5: Order status analysis
SELECT
    status,
    COUNT(*) AS record_count,
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM amazon_sales),
        2
    ) AS percentage_of_records,
    ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_amount
FROM amazon_sales
GROUP BY status
ORDER BY record_count DESC;


-- Query 6: Top 10 products by recorded sales amount
SELECT
    sku,
    category,
    COUNT(*) AS record_count,
    ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_sales_amount
FROM amazon_sales
GROUP BY sku, category
ORDER BY recorded_sales_amount DESC
LIMIT 10;


-- Query 7: Cancellation rate by product category
SELECT
    category,
    COUNT(*) AS total_records,
    SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END)
        AS cancelled_records,
    ROUND(
        100.0 *
        SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        2
    ) AS cancellation_rate_percent
FROM amazon_sales
GROUP BY category
ORDER BY cancellation_rate_percent DESC;


-- Query 8: Monthly order-record counts and recorded sales
-- for each product category
SELECT
    strftime('%Y-%m', date) AS month,
    category,
    COUNT(*) AS order_records,
    ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_sales_amount
FROM amazon_sales
GROUP BY strftime('%Y-%m', date), category
ORDER BY month, recorded_sales_amount DESC;


-- Query 9: Shipping destination performance
SELECT
    ship_state,
    COUNT(*) AS order_records,
    ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_sales_amount
FROM amazon_sales
GROUP BY ship_state
ORDER BY recorded_sales_amount DESC
LIMIT 10;


-- Query 10: Basic data availability checks
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT order_id) AS distinct_order_ids,
    COUNT(DISTINCT sku) AS distinct_skus,
    SUM(CASE WHEN date IS NULL OR date = '' THEN 1 ELSE 0 END)
        AS missing_dates,
    SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)
        AS missing_amounts
FROM amazon_sales;


-- NOTE:
-- This dataset does not contain a customer ID.
-- Customer-level rankings and customer retention rates
-- cannot be calculated reliably from this table alone.
-- Recorded amounts include different order statuses and
-- should not automatically be interpreted as completed revenue.
