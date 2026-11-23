from datetime import date

import pytest

from src.database import connect, get_return_for_order, init_db
from src.order_tools import NOT_FOUND
from src.return_tools import make_return_tool


@pytest.fixture
def conn():
    connection = connect(":memory:")
    init_db(connection)
    return connection


def make_tool(conn, today=date(2026, 10, 20)):
    return make_return_tool(conn, customer_id=1, today=today)


def test_creates_a_pending_return(conn):
    result = make_tool(conn)(1001, "too small")
    assert result["status"] == "pending_confirmation"
    assert get_return_for_order(conn, 1001)["reason"] == "too small"


def test_rejects_after_the_return_window(conn):
    result = make_tool(conn, today=date(2026, 12, 1))(1001, "too small")
    assert "window" in result["error"]
    assert get_return_for_order(conn, 1001) is None


def test_rejects_an_order_that_is_not_delivered(conn):
    result = make_tool(conn)(1002, "changed my mind")
    assert "delivered" in result["error"]


def test_rejects_another_customers_order(conn):
    assert make_tool(conn)(1004, "too small") == NOT_FOUND
    assert get_return_for_order(conn, 1004) is None


def test_unknown_order_is_not_found(conn):
    assert make_tool(conn)(9999, "too small") == NOT_FOUND


def test_second_request_for_the_same_order_is_rejected(conn):
    request_return = make_tool(conn)
    request_return(1001, "too small")
    result = request_return(1001, "too small again")
    assert "already" in result["error"]
