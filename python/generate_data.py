import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

NUM_USERS = 20_000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 6, 30)

OUTPUT_FILE = "data/raw/customer_events.csv"

random.seed(42)
np.random.seed(42)


# -----------------------------
# Reference data
# -----------------------------

categories = [
    "Electronics",
    "Clothing",
    "Home",
    "Beauty",
    "Sports",
]

devices = [
    "Desktop",
    "Mobile",
    "Tablet",
]

countries = [
    "UK",
    "USA",
    "Canada",
    "Germany",
    "Australia",
]

traffic_sources = [
    "Organic",
    "Paid Search",
    "Social",
    "Email",
    "Direct",
]

products = {
    "Electronics": ["ELEC001", "ELEC002", "ELEC003", "ELEC004"],
    "Clothing": ["CLO001", "CLO002", "CLO003", "CLO004"],
    "Home": ["HOME001", "HOME002", "HOME003", "HOME004"],
    "Beauty": ["BEAU001", "BEAU002", "BEAU003", "BEAU004"],
    "Sports": ["SPORT001", "SPORT002", "SPORT003", "SPORT004"],
}


# -----------------------------
# Helper functions
# -----------------------------

def random_timestamp():
    total_seconds = int((END_DATE - START_DATE).total_seconds())

    random_seconds = random.randint(0, total_seconds)

    return START_DATE + timedelta(seconds=random_seconds)


def choose_variant():
    return random.choice(["Control", "Variant"])


def choose_category():
    return random.choice(categories)


def choose_device():
    return random.choices(
        devices,
        weights=[0.30, 0.55, 0.15],
        k=1,
    )[0]


def choose_country():
    return random.choices(
        countries,
        weights=[0.40, 0.25, 0.12, 0.13, 0.10],
        k=1,
    )[0]


def choose_traffic_source():
    return random.choices(
        traffic_sources,
        weights=[0.30, 0.25, 0.20, 0.10, 0.15],
        k=1,
    )[0]


def choose_price(category):
    price_ranges = {
        "Electronics": (50, 1200),
        "Clothing": (20, 250),
        "Home": (25, 500),
        "Beauty": (10, 180),
        "Sports": (20, 400),
    }

    low, high = price_ranges[category]

    return round(random.uniform(low, high), 2)


# -----------------------------
# Generate customer journeys
# -----------------------------

events = []

for user_id in range(1, NUM_USERS + 1):

    session_id = f"sess_{user_id}_{random.randint(1, 3)}"

    session_start = random_timestamp()

    device = choose_device()
    country = choose_country()
    traffic_source = choose_traffic_source()
    variant = choose_variant()
    category = choose_category()

    product_id = random.choice(products[category])

    price = choose_price(category)

    # Mobile users have slightly lower purchase probability.
    # Variant users have slightly higher purchase probability.
    purchase_probability = 0.22

    if device == "Mobile":
        purchase_probability -= 0.05

    if variant == "Variant":
        purchase_probability += 0.04

    # Traffic source differences
    if traffic_source == "Email":
        purchase_probability += 0.05

    if traffic_source == "Social":
        purchase_probability -= 0.03

    # Keep probability within sensible bounds
    purchase_probability = max(
        0.05,
        min(purchase_probability, 0.60),
    )

    # Every user starts with a visit
    current_time = session_start

    events.append(
        {
            "user_id": user_id,
            "session_id": session_id,
            "event_timestamp": current_time,
            "event_type": "visit",
            "product_id": None,
            "category": None,
            "device": device,
            "country": country,
            "traffic_source": traffic_source,
            "experiment_variant": variant,
            "price": None,
        }
    )

    # Some visitors never reach a product page
    if random.random() < 0.20:
        continue

    current_time += timedelta(seconds=random.randint(20, 180))

    events.append(
        {
            "user_id": user_id,
            "session_id": session_id,
            "event_timestamp": current_time,
            "event_type": "product_view",
            "product_id": product_id,
            "category": category,
            "device": device,
            "country": country,
            "traffic_source": traffic_source,
            "experiment_variant": variant,
            "price": price,
        }
    )

    # Some visitors leave after viewing a product
    if random.random() < 0.30:
        continue

    current_time += timedelta(seconds=random.randint(30, 240))

    events.append(
        {
            "user_id": user_id,
            "session_id": session_id,
            "event_timestamp": current_time,
            "event_type": "add_to_cart",
            "product_id": product_id,
            "category": category,
            "device": device,
            "country": country,
            "traffic_source": traffic_source,
            "experiment_variant": variant,
            "price": price,
        }
    )

    # Some customers abandon their cart
    if random.random() < 0.25:
        continue

    current_time += timedelta(seconds=random.randint(30, 300))

    events.append(
        {
            "user_id": user_id,
            "session_id": session_id,
            "event_timestamp": current_time,
            "event_type": "checkout",
            "product_id": product_id,
            "category": category,
            "device": device,
            "country": country,
            "traffic_source": traffic_source,
            "experiment_variant": variant,
            "price": price,
        }
    )

    # Final purchase decision
    if random.random() > purchase_probability:
        continue

    current_time += timedelta(seconds=random.randint(30, 300))

    events.append(
        {
            "user_id": user_id,
            "session_id": session_id,
            "event_timestamp": current_time,
            "event_type": "purchase",
            "product_id": product_id,
            "category": category,
            "device": device,
            "country": country,
            "traffic_source": traffic_source,
            "experiment_variant": variant,
            "price": price,
        }
    )


# -----------------------------
# Create DataFrame
# -----------------------------

df = pd.DataFrame(events)

df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])

df = df.sort_values(
    ["event_timestamp", "user_id"]
).reset_index(drop=True)

df.insert(
    0,
    "event_id",
    range(1, len(df) + 1),
)


# -----------------------------
# Save dataset
# -----------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False,
)


# -----------------------------
# Print summary
# -----------------------------

print("Dataset generated successfully!")
print(f"Rows: {len(df):,}")
print(f"Users: {df['user_id'].nunique():,}")
print(f"Sessions: {df['session_id'].nunique():,}")
print()
print("Event counts:")
print(df["event_type"].value_counts())
print()
print(f"Saved to: {OUTPUT_FILE}")