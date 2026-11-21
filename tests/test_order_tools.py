import pytest

from src.database import connect, init_db
from src.order_tools import NOT_FOUND, make_order_tools


@pytest.fixture
def conn():
    connection = connect(":memory:")
    init_db(connection)
    return connection


@pytest.fixture
def tools(conn):
    return make_order_tools(conn, customer_id=1)


def test_returns_own_order(tools):
    get_order_status, _ = tools
    order = get_order_status(1001)
    assert order["product"] == "Wireless Headphones"
    assert order["status"] == "delivered"


def test_other_customers_order_is_hidden(tools):
    get_order_status, _ = tools
    assert get_order_status(1003) == NOT_FOUND


def test_unknown_order_looks_the_same_as_a_hidden_one(tools):
    get_order_status, _ = tools
    assert get_order_status(9999) == get_order_status(1003)


def test_order_view_does_not_expose_customer_id(tools):
    get_order_status, list_my_orders = tools
    assert "customer_id" not in get_order_status(1001)
    assert all("customer_id" not in order for order in list_my_orders())


def test_lists_only_own_orders_newest_first(tools):
    _, list_my_orders = tools
    assert [order["id"] for order in list_my_orders()] == [1002, 1001]


def test_tools_are_bound_to_the_customer(conn):
    get_order_status, list_my_orders = make_order_tools(conn, customer_id=2)
    assert get_order_status(1003)["product"] == "Running Shoes"
    assert get_order_status(1001) == NOT_FOUND
    assert {order["id"] for order in list_my_orders()} == {1003, 1004}
