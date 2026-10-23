-- TASK 2: SQL VIEWS AND INDEXING
-- Database: SQLite

-- View 1: Monthly recorded sales
CREATE VIEW IF NOT EXISTS vw_monthly_sales AS
SELECT
    strftime('%Y-%m', date) AS month,
    COUNT(*) AS order_records,
    ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_sales
FROM amazon_sales
GROUP BY strftime('%Y-%m', date);

-- View 2: Product category performance
CREATE VIEW IF NOT EXISTS vw_category_performance AS
SELECT
    category,
    COUNT(*) AS order_records,
    SUM(qty) AS total_recorded_quantity,
    ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_sales,
    ROUND(AVG(amount), 2) AS average_amount
FROM amazon_sales
GROUP BY category;

-- View 3: Order status summary
CREATE VIEW IF NOT EXISTS vw_order_status_summary AS
SELECT
    status,
    COUNT(*) AS order_records,
    ROUND(SUM(COALESCE(amount, 0)), 2) AS recorded_amount
FROM amazon_sales
GROUP BY status;

-- Indexes for common filtering, grouping and lookup operations.
CREATE INDEX IF NOT EXISTS idx_amazon_sales_date
ON amazon_sales(date);

CREATE INDEX IF NOT EXISTS idx_amazon_sales_category
ON amazon_sales(category);

CREATE INDEX IF NOT EXISTS idx_amazon_sales_status
ON amazon_sales(status);

CREATE INDEX IF NOT EXISTS idx_amazon_sales_sku
ON amazon_sales(sku);
