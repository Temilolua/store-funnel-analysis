CREATE TABLE customer_events (
    event_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    session_id VARCHAR(50) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    event_type VARCHAR(30) NOT NULL,
    product_id VARCHAR(50),
    category VARCHAR(50),
    device VARCHAR(20),
    country VARCHAR(50),
    traffic_source VARCHAR(50),
    experiment_variant VARCHAR(20),
    price NUMERIC(10, 2)
);