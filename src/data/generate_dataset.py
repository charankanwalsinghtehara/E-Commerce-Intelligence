import os
import random
import sqlite3
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# -----------------------------
# Reproducibility
# -----------------------------
random.seed(42)
np.random.seed(42)


# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
DATABASE_DIR = os.path.join(BASE_DIR, "database")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(DATABASE_DIR, exist_ok=True)


# -----------------------------
# Configuration
# -----------------------------
NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 300
NUM_ORDERS = 30000

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 31)


# -----------------------------
# Helper functions
# -----------------------------
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


def random_name():
    first_names = [
        "Aarav", "Arjun", "Kabir", "Vihaan", "Aditya",
        "Rohan", "Rahul", "Karan", "Simran", "Ananya",
        "Priya", "Meera", "Aisha", "Ishita", "Neha"
    ]

    last_names = [
        "Sharma", "Singh", "Kaur", "Kumar", "Gupta",
        "Patel", "Verma", "Mehta", "Malhotra", "Gill"
    ]

    return random.choice(first_names) + " " + random.choice(last_names)


# -----------------------------
# Locations
# -----------------------------
locations = [
    ("Chandigarh", "Chandigarh"),
    ("Mohali", "Punjab"),
    ("Kharar", "Punjab"),
    ("Ludhiana", "Punjab"),
    ("Amritsar", "Punjab"),
    ("Jalandhar", "Punjab"),
    ("Delhi", "Delhi"),
    ("Gurgaon", "Haryana"),
    ("Noida", "Uttar Pradesh"),
    ("Jaipur", "Rajasthan"),
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Bangalore", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Chennai", "Tamil Nadu"),
    ("Kolkata", "West Bengal"),
]


# -----------------------------
# 1. CUSTOMERS
# -----------------------------
customers = []

for i in range(1, NUM_CUSTOMERS + 1):

    city, state = random.choice(locations)

    customers.append({
        "customer_id": i,
        "customer_name": random_name(),
        "gender": random.choice(["Male", "Female"]),
        "age": random.randint(18, 65),
        "city": city,
        "state": state,
        "country": "India",
        "signup_date": random_date(
            datetime(2022, 1, 1),
            datetime(2025, 6, 30)
        ).date()
    })

customers_df = pd.DataFrame(customers)


# -----------------------------
# 2. PRODUCTS
# -----------------------------
categories = {
    "Electronics": [
        "Smartphones",
        "Laptops",
        "Headphones",
        "Smart Watches",
        "Accessories"
    ],
    "Home": [
        "Furniture",
        "Kitchen",
        "Decor",
        "Storage"
    ],
    "Fashion": [
        "Men Clothing",
        "Women Clothing",
        "Footwear",
        "Accessories"
    ],
    "Beauty": [
        "Skincare",
        "Haircare",
        "Makeup",
        "Personal Care"
    ],
    "Sports": [
        "Fitness",
        "Outdoor",
        "Sportswear",
        "Equipment"
    ]
}

products = []

product_id = 1

for category, subcategories in categories.items():

    for subcategory in subcategories:

        products_per_subcategory = NUM_PRODUCTS // sum(
            len(x) for x in categories.values()
        )

        for _ in range(products_per_subcategory):

            unit_cost = round(random.uniform(200, 30000), 2)

            margin = random.uniform(1.15, 1.80)

            unit_price = round(unit_cost * margin, 2)

            products.append({
                "product_id": product_id,
                "product_name": f"{subcategory} Product {product_id}",
                "category": category,
                "sub_category": subcategory,
                "unit_cost": unit_cost,
                "unit_price": unit_price
            })

            product_id += 1

products_df = pd.DataFrame(products)


# -----------------------------
# 3. ORDERS + ORDER ITEMS
# -----------------------------
orders = []
order_items = []

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery"
]

order_statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Cancelled",
    "Returned"
]

order_item_id = 1

for order_id in range(1, NUM_ORDERS + 1):

    customer_id = random.randint(1, NUM_CUSTOMERS)

    order_date = random_date(START_DATE, END_DATE)

    customer = customers_df.iloc[customer_id - 1]

    product_count = random.randint(1, 4)

    selected_products = random.sample(
        range(1, len(products_df) + 1),
        product_count
    )

    status = random.choice(order_statuses)

    orders.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": order_date.date(),
        "payment_method": random.choice(payment_methods),
        "shipping_city": customer["city"],
        "shipping_state": customer["state"],
        "order_status": status
    })

    for product_id in selected_products:

        quantity = random.randint(1, 4)

        discount = round(
            random.choice([0, 0.05, 0.10, 0.15, 0.20]),
            2
        )

        order_items.append({
            "order_item_id": order_item_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "discount": discount
        })

        order_item_id += 1


orders_df = pd.DataFrame(orders)
order_items_df = pd.DataFrame(order_items)


# -----------------------------
# 4. SAVE RAW CSV FILES
# -----------------------------
customers_df.to_csv(
    os.path.join(RAW_DIR, "customers.csv"),
    index=False
)

products_df.to_csv(
    os.path.join(RAW_DIR, "products.csv"),
    index=False
)

orders_df.to_csv(
    os.path.join(RAW_DIR, "orders.csv"),
    index=False
)

order_items_df.to_csv(
    os.path.join(RAW_DIR, "order_items.csv"),
    index=False
)


# -----------------------------
# 5. CREATE SQLITE DATABASE
# -----------------------------
database_path = os.path.join(
    DATABASE_DIR,
    "ecommerce.db"
)

connection = sqlite3.connect(database_path)

customers_df.to_sql(
    "customers",
    connection,
    if_exists="replace",
    index=False
)

products_df.to_sql(
    "products",
    connection,
    if_exists="replace",
    index=False
)

orders_df.to_sql(
    "orders",
    connection,
    if_exists="replace",
    index=False
)

order_items_df.to_sql(
    "order_items",
    connection,
    if_exists="replace",
    index=False
)

connection.close()


# -----------------------------
# 6. SUMMARY
# -----------------------------
print("=" * 60)
print("E-COMMERCE DATASET CREATED SUCCESSFULLY")
print("=" * 60)

print(f"Customers   : {len(customers_df):,}")
print(f"Products    : {len(products_df):,}")
print(f"Orders      : {len(orders_df):,}")
print(f"Order Items : {len(order_items_df):,}")

print()
print("Files created:")
print("data/raw/customers.csv")
print("data/raw/products.csv")
print("data/raw/orders.csv")
print("data/raw/order_items.csv")
print("database/ecommerce.db")

print("=" * 60)