import os
import sqlite3
import pandas as pd


# ============================================
# 1. PROJECT PATHS
# ============================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "ecommerce.db"
)


# ============================================
# 2. LOAD CLEAN CSV FILES
# ============================================

customers = pd.read_csv(
    os.path.join(
        PROCESSED_DIR,
        "customers_clean.csv"
    )
)

products = pd.read_csv(
    os.path.join(
        PROCESSED_DIR,
        "products_clean.csv"
    )
)

orders = pd.read_csv(
    os.path.join(
        PROCESSED_DIR,
        "orders_clean.csv"
    )
)

order_items = pd.read_csv(
    os.path.join(
        PROCESSED_DIR,
        "order_items_clean.csv"
    )
)


# ============================================
# 3. CONNECT TO SQLITE
# ============================================

connection = sqlite3.connect(
    DATABASE_PATH
)


# ============================================
# 4. LOAD DATA INTO TABLES
# ============================================

customers.to_sql(
    "customers",
    connection,
    if_exists="replace",
    index=False
)

products.to_sql(
    "products",
    connection,
    if_exists="replace",
    index=False
)

orders.to_sql(
    "orders",
    connection,
    if_exists="replace",
    index=False
)

order_items.to_sql(
    "order_items",
    connection,
    if_exists="replace",
    index=False
)


# ============================================
# 5. CREATE INDEXES
# ============================================

cursor = connection.cursor()

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_orders_customer
ON orders(customer_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_order_items_order
ON order_items(order_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_order_items_product
ON order_items(product_id)
""")


connection.commit()


# ============================================
# 6. VERIFY TABLES
# ============================================

tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """,
    connection
)

print("\nDATABASE TABLES:")
print(tables)


# ============================================
# 7. ROW COUNTS
# ============================================

for table in [
    "customers",
    "products",
    "orders",
    "order_items"
]:

    result = pd.read_sql_query(
        f"SELECT COUNT(*) AS total FROM {table}",
        connection
    )

    print(
        f"{table}: {result['total'].iloc[0]:,} rows"
    )


connection.close()

print("\nDATABASE LOADED SUCCESSFULLY!")