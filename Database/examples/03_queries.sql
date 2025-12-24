-- Database 101 - Example 3: Common SQL Queries
-- Practice queries for the e-commerce database

-- ============================================
-- BASIC SELECT QUERIES
-- ============================================

-- Get all products
SELECT * FROM products;

-- Get specific columns
SELECT name, price, stock_quantity FROM products;

-- Filter with WHERE
SELECT name, price
FROM products
WHERE category = 'Electronics';

-- Multiple conditions with AND/OR
SELECT name, price, stock_quantity
FROM products
WHERE category = 'Electronics'
  AND price < 100
  AND stock_quantity > 50;

-- Sort results
SELECT name, price
FROM products
ORDER BY price DESC;  -- DESC = descending, ASC = ascending

-- Limit results
SELECT name, price
FROM products
ORDER BY price DESC
LIMIT 5;

-- Pattern matching with LIKE
SELECT first_name, last_name, email
FROM customers
WHERE email LIKE '%@gmail.com';

-- BETWEEN for ranges
SELECT name, price
FROM products
WHERE price BETWEEN 50 AND 200;

-- IN for multiple values
SELECT name, price
FROM products
WHERE category IN ('Electronics', 'Home Office');

-- ============================================
-- AGGREGATION QUERIES
-- ============================================

-- Count records
SELECT COUNT(*) AS total_products FROM products;

-- Count by category
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category
ORDER BY product_count DESC;

-- Sum, Average, Min, Max
SELECT
    COUNT(*) AS total_products,
    SUM(stock_quantity) AS total_stock,
    AVG(price) AS average_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM products;

-- Aggregation by category
SELECT
    category,
    COUNT(*) AS product_count,
    AVG(price)::DECIMAL(10,2) AS avg_price,
    SUM(stock_quantity) AS total_stock
FROM products
GROUP BY category
ORDER BY avg_price DESC;

-- HAVING clause (filter after GROUP BY)
SELECT
    category,
    COUNT(*) AS product_count,
    AVG(price)::DECIMAL(10,2) AS avg_price
FROM products
GROUP BY category
HAVING COUNT(*) > 2
ORDER BY avg_price DESC;

-- ============================================
-- JOIN QUERIES
-- ============================================

-- INNER JOIN: Orders with customer names
SELECT
    o.id AS order_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    o.order_date,
    o.status,
    o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
ORDER BY o.order_date DESC;

-- LEFT JOIN: All customers, even without orders
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(o.id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.first_name, c.last_name
ORDER BY total_spent DESC;

-- Multiple JOINs: Full order details
SELECT
    o.id AS order_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price,
    oi.subtotal
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
ORDER BY o.id, p.name;

-- ============================================
-- BUSINESS ANALYTICS QUERIES
-- ============================================

-- Top selling products
SELECT
    p.name AS product_name,
    p.category,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.subtotal) AS total_revenue
FROM products p
INNER JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id, p.name, p.category
ORDER BY total_revenue DESC
LIMIT 10;

-- Best customers
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    COUNT(DISTINCT o.id) AS order_count,
    SUM(o.total_amount) AS total_spent
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.first_name, c.last_name, c.email
ORDER BY total_spent DESC
LIMIT 5;

-- Revenue by category
SELECT
    p.category,
    COUNT(DISTINCT oi.id) AS items_sold,
    SUM(oi.subtotal) AS category_revenue,
    ROUND(SUM(oi.subtotal) / (SELECT SUM(subtotal) FROM order_items) * 100, 2) AS percentage
FROM products p
INNER JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;

-- Orders by status
SELECT
    status,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_value
FROM orders
GROUP BY status
ORDER BY order_count DESC;

-- Monthly sales (if you have date data)
SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS monthly_revenue
FROM orders
WHERE status IN ('delivered', 'shipped')
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month DESC;

-- ============================================
-- LAST 10 ORDERS FOR A PRODUCT (with product details)
-- ============================================

-- Example: Get last 10 orders for 'Laptop Pro'
SELECT
    p.id AS product_id,
    p.name AS product_name,
    p.price AS current_price,
    p.category,
    p.stock_quantity AS current_stock,
    o.id AS order_id,
    o.order_date,
    o.status AS order_status,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city AS customer_city,
    oi.quantity,
    oi.unit_price AS price_at_purchase,
    oi.subtotal
FROM products p
INNER JOIN order_items oi ON p.id = oi.product_id
INNER JOIN orders o ON oi.order_id = o.id
INNER JOIN customers c ON o.customer_id = c.id
WHERE p.name = 'Laptop Pro'
ORDER BY o.order_date DESC
LIMIT 10;

-- Same query using product ID
SELECT
    p.id AS product_id,
    p.name AS product_name,
    p.price AS current_price,
    p.category,
    o.id AS order_id,
    o.order_date,
    o.status AS order_status,
    c.first_name || ' ' || c.last_name AS customer_name,
    oi.quantity,
    oi.unit_price AS price_at_purchase,
    oi.subtotal
FROM products p
INNER JOIN order_items oi ON p.id = oi.product_id
INNER JOIN orders o ON oi.order_id = o.id
INNER JOIN customers c ON o.customer_id = c.id
WHERE p.id = 1  -- Product ID for Laptop Pro
ORDER BY o.order_date DESC
LIMIT 10;

-- ============================================
-- LOW STOCK ALERT
-- ============================================

-- Products that need reordering (stock < 50)
SELECT
    name,
    sku,
    category,
    stock_quantity,
    CASE
        WHEN stock_quantity < 20 THEN 'CRITICAL'
        WHEN stock_quantity < 50 THEN 'LOW'
        ELSE 'OK'
    END AS stock_status
FROM products
WHERE stock_quantity < 50
ORDER BY stock_quantity;
