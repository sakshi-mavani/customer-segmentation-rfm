-- RFM Analysis Query 
-- This query calculatess Recency, Frequency, and Monetary values for each customer 

WITH order_summary As (
    SELECT
        c.customer_unique_id,
        o.order_id,
        o.order_purchase_timestamp,
        oi.price
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
)

SELECT 
    customer_unique_id,
    CAST(JULIANDAY('now') - JULIANDAY(MAX(order_purchase_timestamp)) AS INTEGER) AS Recency,
    COUNT(DISTINCT order_id) AS Frequency,
    ROUND(SUM(price), 2) AS Monetary

FROM order_summary
GROUP BY customer_unique_id
ORDER BY Monetary DESC;

