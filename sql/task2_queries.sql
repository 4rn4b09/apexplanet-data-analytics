-- Query 1: Display the first 10 records
SELECT *
FROM amazon_sales
LIMIT 10;


-- Query 2: Count the total number of records
SELECT COUNT(*) AS total_records
FROM amazon_sales;


-- Query 3: Show all product categories
SELECT DISTINCT category
FROM amazon_sales
ORDER BY category;

-- Query 4: Find orders with a quantity greater than 1
SELECT order_id, category, qty, amount
FROM amazon_sales
WHERE qty > 1
ORDER BY qty DESC
LIMIT 10;


-- Query 5: Count records in each product category
SELECT category, COUNT(*) AS total_records
FROM amazon_sales
GROUP BY category
ORDER BY total_records DESC;


-- Query 6: Calculate recorded sales by product category
SELECT
    category,
    ROUND(SUM(amount), 2) AS total_recorded_sales
FROM amazon_sales
GROUP BY category
ORDER BY total_recorded_sales DESC;

-- Query 7: Analyze order records by status
SELECT
    status,
    COUNT(*) AS total_records,
    ROUND(100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM amazon_sales), 2) AS percentage
FROM amazon_sales
GROUP BY status
ORDER BY total_records DESC;

-- Query 8: Calculate average recorded sales amount by category
SELECT
    category,
    ROUND(AVG(amount), 2) AS average_amount,
    COUNT(amount) AS records_with_amount
FROM amazon_sales
GROUP BY category
ORDER BY average_amount DESC;
-- Query 9: Find the top 10 records by amount
SELECT
    order_id,
    category,
    amount,
    status
FROM amazon_sales
WHERE amount IS NOT NULL
ORDER BY amount DESC
LIMIT 10;
-- Query 10: Analyze quantities by product category
SELECT
    category,
    SUM(qty) AS total_quantity,
    ROUND(AVG(qty), 2) AS average_quantity,
    MAX(qty) AS maximum_quantity
FROM amazon_sales
GROUP BY category
ORDER BY total_quantity DESC;
-- Query 11: Count cancelled records by category
SELECT
    category,
    COUNT(*) AS cancelled_records,
    ROUND(100.0 * COUNT(*) /
        (SELECT COUNT(*)
         FROM amazon_sales
         WHERE status = 'Cancelled'), 2) AS percentage_of_cancellations
FROM amazon_sales
WHERE status = 'Cancelled'
GROUP BY category
ORDER BY cancelled_records DESC;
-- Query 12: Calculate cancellation rate by category
SELECT
    category,
    COUNT(*) AS total_records,
    SUM(CASE
        WHEN status = 'Cancelled' THEN 1
        ELSE 0
    END) AS cancelled_records,
    ROUND(
        100.0 * SUM(CASE
            WHEN status = 'Cancelled' THEN 1
            ELSE 0
        END) / COUNT(*),
        2
    ) AS cancellation_rate
FROM amazon_sales
GROUP BY category
ORDER BY cancellation_rate DESC;

    -- Query 13: Recorded sales amount by order status
SELECT
    status,
    COUNT(*) AS total_records,
    ROUND(SUM(amount), 2) AS total_recorded_amount,
    ROUND(AVG(amount), 2) AS average_recorded_amount
FROM amazon_sales
GROUP BY status
ORDER BY total_recorded_amount DESC;
