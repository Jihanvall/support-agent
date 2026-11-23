import sqlite3
from pathlib import Path

DB_PATH = Path("data/shop.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    product TEXT NOT NULL,
    status TEXT NOT NULL,
    total REAL NOT NULL,
    ordered_on TEXT NOT NULL,
    delivered_on TEXT
);
CREATE TABLE IF NOT EXISTS returns (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    created_on TEXT NOT NULL
);
"""

CUSTOMERS = [
    (1, "jihane Vall", "jihane@example.com"),
    (2, "Mulay Ely", "mulay@example.com"),
    (3, "asma Chebby", "asma@example.com"),
]

ORDERS = [
    (1001, 1, "Wireless Headphones", "delivered", 59.90, "2026-10-01", "2026-10-05"),
    (1002, 1, "Phone Case", "processing", 12.50, "2026-11-10", None),
    (1003, 2, "Running Shoes", "shipped", 89.00, "2026-11-08", None),
    (1004, 2, "Backpack", "delivered", 45.00, "2026-10-15", "2026-10-19"),
    (1005, 3, "Coffee Maker", "cancelled", 120.00, "2026-11-02", None),
    (1006, 3, "Desk Lamp", "shipped", 34.99, "2026-11-09", None),
]


def connect(path=DB_PATH):
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    conn.executescript(SCHEMA)
    count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    if count == 0:
        conn.executemany("INSERT INTO customers VALUES (?, ?, ?)", CUSTOMERS)
        conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)", ORDERS)
        conn.commit()


def get_order(conn, order_id):
    row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return dict(row) if row else None


def get_orders_for_customer(conn, customer_id):
    rows = conn.execute(
        "SELECT * FROM orders WHERE customer_id = ? ORDER BY ordered_on DESC",
        (customer_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def create_return(conn, order_id, reason, created_on):
    cursor = conn.execute(
        "INSERT INTO returns (order_id, reason, status, created_on) VALUES (?, ?, 'pending_confirmation', ?)",
        (order_id, reason, created_on),
    )
    conn.commit()
    return cursor.lastrowid


def get_return_for_order(conn, order_id):
    row = conn.execute("SELECT * FROM returns WHERE order_id = ?", (order_id,)).fetchone()
    return dict(row) if row else None


def get_return(conn, return_id):
    row = conn.execute("SELECT * FROM returns WHERE id = ?", (return_id,)).fetchone()
    return dict(row) if row else None


def set_return_status(conn, return_id, status):
    conn.execute("UPDATE returns SET status = ? WHERE id = ?", (status, return_id))
    conn.commit()


if __name__ == "__main__":
    connection = connect()
    init_db(connection)
    print(f"Database ready at {DB_PATH}")
