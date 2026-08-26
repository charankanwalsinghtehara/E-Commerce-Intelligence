import os
import pandas as pd


# ============================================
# 1. SET PROJECT PATHS
# ============================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)


# ============================================
# 2. LOAD RAW DATA
# ============================================

customers = pd.read_csv(
    os.path.join(RAW_DIR, "customers.csv")
)

products = pd.read_csv(
    os.path.join(RAW_DIR, "products.csv")
)

orders = pd.read_csv(
    os.path.join(RAW_DIR, "orders.csv")
)

order_items = pd.read_csv(
    os.path.join(RAW_DIR, "order_items.csv")
)


print("Raw datasets loaded.")


# ============================================
# 3. REMOVE DUPLICATE ROWS
# ============================================

customers = customers.drop_duplicates()
products = products.drop_duplicates()
orders = orders.drop_duplicates()
order_items = order_items.drop_duplicates()


# ============================================
# 4. REMOVE DUPLICATE IDs
# ============================================

customers = customers.drop_duplicates(
    subset=["customer_id"]
)

products = products.drop_duplicates(
    subset=["product_id"]
)

orders = orders.drop_duplicates(
    subset=["order_id"]
)

order_items = order_items.drop_duplicates(
    subset=["order_item_id"]
)


# ============================================
# 5. CONVERT DATE COLUMNS
# ============================================

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"],
    errors="coerce"
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)


# ============================================
# 6. REMOVE INVALID DATE RECORDS
# ============================================

customers = customers.dropna(
    subset=["signup_date"]
)

orders = orders.dropna(
    subset=["order_date"]
)


# ============================================
# 7. STANDARDIZE TEXT
# ============================================

customers["customer_name"] = (
    customers["customer_name"]
    .astype(str)
    .str.strip()
)

customers["gender"] = (
    customers["gender"]
    .astype(str)
    .str.strip()
    .str.title()
)

customers["city"] = (
    customers["city"]
    .astype(str)
    .str.strip()
)

customers["state"] = (
    customers["state"]
    .astype(str)
    .str.strip()
)

products["product_name"] = (
    products["product_name"]
    .astype(str)
    .str.strip()
)

products["category"] = (
    products["category"]
    .astype(str)
    .str.strip()
)

products["sub_category"] = (
    products["sub_category"]
    .astype(str)
    .str.strip()
)

orders["payment_method"] = (
    orders["payment_method"]
    .astype(str)
    .str.strip()
)

orders["order_status"] = (
    orders["order_status"]
    .astype(str)
    .str.strip()
)

orders["shipping_city"] = (
    orders["shipping_city"]
    .astype(str)
    .str.strip()
)

orders["shipping_state"] = (
    orders["shipping_state"]
    .astype(str)
    .str.strip()
)


# ============================================
# 8. VALIDATE NUMERICAL VALUES
# ============================================

customers = customers[
    (customers["age"] >= 18) &
    (customers["age"] <= 100)
]

products = products[
    (products["unit_cost"] >= 0) &
    (products["unit_price"] >= 0)
]

order_items = order_items[
    (order_items["quantity"] > 0) &
    (order_items["discount"] >= 0) &
    (order_items["discount"] <= 1)
]


# ============================================
# 9. VALIDATE RELATIONSHIPS
# ============================================

orders = orders[
    orders["customer_id"].isin(
        customers["customer_id"]
    )
]

order_items = order_items[
    order_items["order_id"].isin(
        orders["order_id"]
    )
]

order_items = order_items[
    order_items["product_id"].isin(
        products["product_id"]
    )
]


# ============================================
# 10. CREATE PRODUCT PROFIT
# ============================================

products["profit_per_unit"] = (
    products["unit_price"] -
    products["unit_cost"]
)

products["profit_margin"] = (
    products["profit_per_unit"] /
    products["unit_price"]
)


# ============================================
# 11. SAVE CLEAN DATA
# ============================================

customers.to_csv(
    os.path.join(PROCESSED_DIR, "customers_clean.csv"),
    index=False
)

products.to_csv(
    os.path.join(PROCESSED_DIR, "products_clean.csv"),
    index=False
)

orders.to_csv(
    os.path.join(PROCESSED_DIR, "orders_clean.csv"),
    index=False
)

order_items.to_csv(
    os.path.join(PROCESSED_DIR, "order_items_clean.csv"),
    index=False
)


# ============================================
# 12. FINAL SUMMARY
# ============================================

print()
print("=" * 55)
print("DATA CLEANING COMPLETED")
print("=" * 55)

print(f"Customers   : {len(customers):,}")
print(f"Products    : {len(products):,}")
print(f"Orders      : {len(orders):,}")
print(f"Order Items : {len(order_items):,}")

print()
print("Clean files saved in:")
print("data/processed/")

print("=" * 55)