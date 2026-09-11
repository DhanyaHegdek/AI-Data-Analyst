-- =====================================================
-- AI Data Analyst
-- Basic Analytical Queries
-- =====================================================

-- Query 1:
-- Top 5 products by revenue

SELECT
    p.name AS product,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM products p
JOIN order_items oi
    ON p.id = oi.product_id
JOIN orders o
    ON oi.order_id = o.id
GROUP BY p.id, p.name
ORDER BY revenue DESC
LIMIT 5;


-- Query 2:
-- Monthly revenue

SELECT
    DATE_TRUNC('month', o.order_date) AS month,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM orders o
JOIN order_items oi
    ON o.id = oi.order_id
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month;



-- Query 3:
-- Revenue by product category

SELECT
    c.name AS category,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM categories c
JOIN products p
    ON c.id = p.category_id
JOIN order_items oi
    ON p.id = oi.product_id
GROUP BY c.id, c.name
ORDER BY revenue DESC;


-- Query 4:
-- Average order value

SELECT
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM orders
WHERE status != 'cancelled';



-- Query 5:
-- Order count by status

SELECT
    status,
    COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;