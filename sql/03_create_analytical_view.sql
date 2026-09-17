-- ShopSphere
-- Reusable session-level analytical view

CREATE OR REPLACE VIEW session_funnel AS

SELECT
    session_id,
    MAX(user_id) AS user_id,
    MAX(device) AS device,
    MAX(country) AS country,
    MAX(traffic_source) AS traffic_source,
    MAX(category) AS category,
    MAX(experiment_variant) AS experiment_variant,

    MAX(CASE WHEN event_type = 'visit' THEN 1 ELSE 0 END) AS visited,

    MAX(CASE WHEN event_type = 'product_view' THEN 1 ELSE 0 END) AS viewed_product,

    MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) AS added_to_cart,

    MAX(CASE WHEN event_type = 'checkout' THEN 1 ELSE 0 END) AS started_checkout,

    MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased,

    SUM(
        CASE
            WHEN event_type = 'purchase' THEN price
            ELSE 0
        END
    ) AS revenue

FROM customer_events

GROUP BY session_id;