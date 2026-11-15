import pytest

from src.database import connect, get_order, get_orders_for_customer, init_db


@pytest.fixture
def conn():
    connection = connect(":memory:")
    init_db(connection)
    return connection


def test_seed_creates_customers_and_orders(conn):
    customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    assert customers == 3
    assert orders == 6


def test_init_db_twice_does_not_duplicate(conn):
    init_db(conn)
    orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    assert orders == 6


def test_get_order_returns_the_order(conn):
    order = get_order(conn, 1003)
    assert order["product"] == "Running Shoes"
    assert order["status"] == "shipped"
    assert order["customer_id"] == 2


def test_get_order_unknown_returns_none(conn):
    assert get_order(conn, 9999) is None


def test_get_orders_for_customer_newest_first(conn):
    orders = get_orders_for_customer(conn, 1)
    assert [o["id"] for o in orders] == [1002, 1001]


def test_get_orders_for_unknown_customer_is_empty(conn):
    assert get_orders_for_customer(conn, 999) == []
