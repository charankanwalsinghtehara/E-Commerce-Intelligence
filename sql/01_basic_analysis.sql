SELECT *
FROM customers
LIMIT 10;



SELECT COUNT(*) AS total_customers
FROM customers;



SELECT COUNT(*) AS total_products
FROM products;


SELECT COUNT(*) AS total_orders
FROM orders;


SELECT
    SUM(
        p.unit_price
        * oi.quantity
        * (1 - oi.discount)
    ) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id;



SELECT
    SUM(
        (
            p.unit_price * oi.quantity * (1 - oi.discount)
        )
        -
        (
            p.unit_cost * oi.quantity
        )
    ) AS total_profit
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id;



SELECT
    p.category,
    SUM(
        p.unit_price
        * oi.quantity
        * (1 - oi.discount)
    ) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;



SELECT
    o.shipping_state,
    SUM(
        p.unit_price
        * oi.quantity
        * (1 - oi.discount)
    ) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY o.shipping_state
ORDER BY revenue DESC;



SELECT
    ROUND(
        SUM(
            p.unit_price
            * oi.quantity
            * (1 - oi.discount)
        ),
        2
    ) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id;



SELECT
    ROUND(
        SUM(
            (
                p.unit_price * oi.quantity * (1 - oi.discount)
            )
            -
            (
                p.unit_cost * oi.quantity
            )
        ),
        2
    ) AS total_profit
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id;


SELECT
    COUNT(*) AS total_orders
FROM orders;


SELECT
    COUNT(*) AS total_customers
FROM customers;


SELECT
    COUNT(*) AS total_products
FROM products;


SELECT
    ROUND(
        SUM(
            p.unit_price
            * oi.quantity
            * (1 - oi.discount)
        )
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id;



SELECT
    strftime('%Y-%m', o.order_date) AS month,

    ROUND(
        SUM(
            p.unit_price
            * oi.quantity
            * (1 - oi.discount)
        ),
        2
    ) AS revenue

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

GROUP BY month

ORDER BY month;



SELECT
    strftime('%Y-%m', o.order_date) AS month,

    ROUND(
        SUM(
            (
                p.unit_price * oi.quantity * (1 - oi.discount)
            )
            -
            (
                p.unit_cost * oi.quantity
            )
        ),
        2
    ) AS profit

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

GROUP BY month

ORDER BY month;


SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS total_orders

FROM orders

GROUP BY month

ORDER BY month;



SELECT
    p.category,

    ROUND(
        SUM(
            p.unit_price
            * oi.quantity
            * (1 - oi.discount)
        ),
        2
    ) AS revenue

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

GROUP BY p.category

ORDER BY revenue DESC;


SELECT
    p.category,

    ROUND(
        SUM(
            (
                p.unit_price * oi.quantity * (1 - oi.discount)
            )
            -
            (
                p.unit_cost * oi.quantity
            )
        ),
        2
    ) AS profit

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

GROUP BY p.category

ORDER BY profit DESC;



SELECT
    p.product_id,
    p.product_name,

    SUM(oi.quantity) AS units_sold,

    ROUND(
        SUM(
            p.unit_price
            * oi.quantity
            * (1 - oi.discount)
        ),
        2
    ) AS revenue

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

GROUP BY
    p.product_id,
    p.product_name

ORDER BY revenue DESC

LIMIT 10;




SELECT
    c.customer_id,
    c.customer_name,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(
        SUM(
            p.unit_price
            * oi.quantity
            * (1 - oi.discount)
        ),
        2
    ) AS total_spent

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

GROUP BY
    c.customer_id,
    c.customer_name

ORDER BY total_spent DESC

LIMIT 10;

SELECT
    o.shipping_state,

    ROUND(
        SUM(
            p.unit_price
            * oi.quantity
            * (1 - oi.discount)
        ),
        2
    ) AS revenue

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

GROUP BY o.shipping_state

ORDER BY revenue DESC;


SELECT
    payment_method,
    COUNT(*) AS total_orders

FROM orders

GROUP BY payment_method

ORDER BY total_orders DESC;

SELECT
    order_status,
    COUNT(*) AS total_orders

FROM orders

GROUP BY order_status

ORDER BY total_orders DESC;


