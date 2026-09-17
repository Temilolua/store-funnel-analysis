-- ShopSphere Funnel Analysis
-- Overall funnel performance

WITH session_funnel AS (
    SELECT
        session_id,

        MAX(CASE WHEN event_type = 'visit' THEN 1 ELSE 0 END) AS visited,
        MAX(CASE WHEN event_type = 'product_view' THEN 1 ELSE 0 END) AS viewed_product,
        MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) AS added_to_cart,
        MAX(CASE WHEN event_type = 'checkout' THEN 1 ELSE 0 END) AS started_checkout,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased

    FROM customer_events
    GROUP BY session_id
)

SELECT
    SUM(visited) AS visits,
    SUM(viewed_product) AS product_views,
    SUM(added_to_cart) AS add_to_carts,
    SUM(started_checkout) AS checkouts,
    SUM(purchased) AS purchases,

    ROUND(
        100.0 * SUM(viewed_product) / SUM(visited),
        2
    ) AS visit_to_product_pct,

    ROUND(
        100.0 * SUM(added_to_cart) / SUM(viewed_product),
        2
    ) AS product_to_cart_pct,

    ROUND(
        100.0 * SUM(started_checkout) / SUM(added_to_cart),
        2
    ) AS cart_to_checkout_pct,

    ROUND(
        100.0 * SUM(purchased) / SUM(started_checkout),
        2
    ) AS checkout_to_purchase_pct,

    ROUND(
        100.0 * SUM(purchased) / SUM(visited),
        2
    ) AS overall_conversion_pct

FROM session_funnel;

-- Conversion by device, checking to see which device users reach the payment stage the most.

WITH session_funnel AS (
    SELECT
        session_id,
        MAX(device) AS device,

        MAX(CASE WHEN event_type = 'visit' THEN 1 ELSE 0 END) AS visited,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased

    FROM customer_events
    GROUP BY session_id
)

SELECT
    device,
    COUNT(*) AS sessions,
    SUM(purchased) AS purchases,

    ROUND(
        100.0 * SUM(purchased) / COUNT(*),
        2
    ) AS conversion_rate_pct

FROM session_funnel
GROUP BY device
ORDER BY conversion_rate_pct DESC;

-- Conversion by traffic source

WITH session_funnel AS (
    SELECT
        session_id,
        MAX(traffic_source) AS traffic_source,

        MAX(CASE WHEN event_type = 'visit' THEN 1 ELSE 0 END) AS visited,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased

    FROM customer_events
    GROUP BY session_id
)

SELECT
    traffic_source,
    COUNT(*) AS sessions,
    SUM(purchased) AS purchases,

    ROUND(
        100.0 * SUM(purchased) / COUNT(*),
        2
    ) AS conversion_rate_pct

FROM session_funnel
GROUP BY traffic_source
ORDER BY conversion_rate_pct DESC;

WITH session_funnel AS (
    SELECT
        session_id,
        MAX(country) AS country,

        MAX(CASE WHEN event_type = 'visit' THEN 1 ELSE 0 END) AS visited,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased

    FROM customer_events
    GROUP BY session_id
)

SELECT
    country,
    COUNT(*) AS sessions,
    SUM(purchased) AS purchases,

    ROUND(
        100.0 * SUM(purchased) / COUNT(*),
        2
    ) AS conversion_rate_pct

FROM session_funnel
GROUP BY country
ORDER BY conversion_rate_pct DESC;

WITH session_funnel AS (
    SELECT
        session_id,
        MAX(category) AS category,

        MAX(CASE WHEN event_type = 'product_view' THEN 1 ELSE 0 END) AS viewed_product,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased

    FROM customer_events
    GROUP BY session_id
)

SELECT
    category,
    COUNT(*) AS product_sessions,
    SUM(purchased) AS purchases,

    ROUND(
        100.0 * SUM(purchased) / COUNT(*),
        2
    ) AS conversion_rate_pct

FROM session_funnel
WHERE viewed_product = 1
GROUP BY category
ORDER BY conversion_rate_pct DESC;

-- Conversion by device and traffic source

WITH session_funnel AS (
    SELECT
        session_id,
        MAX(device) AS device,
        MAX(traffic_source) AS traffic_source,

        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased

    FROM customer_events
    GROUP BY session_id
)

SELECT
    device,
    traffic_source,
    COUNT(*) AS sessions,
    SUM(purchased) AS purchases,

    ROUND(
        100.0 * SUM(purchased) / COUNT(*),
        2
    ) AS conversion_rate_pct

FROM session_funnel
GROUP BY device, traffic_source
ORDER BY device, conversion_rate_pct DESC;

-- Revenue and Average Order Value

SELECT
    SUM(revenue) AS total_revenue,
    SUM(purchased) AS purchases,

    ROUND(
        SUM(revenue) / NULLIF(SUM(purchased), 0),
        2
    ) AS average_order_value

FROM session_funnel;